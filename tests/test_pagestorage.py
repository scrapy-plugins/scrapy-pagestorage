import os
import types
from unittest import mock, TestCase

from scrapy import Spider, signals
from scrapy.http import Request, Response, TextResponse
from scrapy.item import Item
from scrapy.settings import Settings
from scrapy.exceptions import NotConfigured, IgnoreRequest
from scrapy.utils.request import request_fingerprint

from scrapy_pagestorage import _get_enabled_status, PageStorageMiddleware


def test_get_enabled_status():
    settings = Settings()
    # check for void settings
    assert _get_enabled_status(settings) == (False, False)
    # plugin enabled with settings
    settings.set('PAGE_STORAGE_ENABLED', True)
    assert _get_enabled_status(settings) == (True, False)
    settings.set('PAGE_STORAGE_ENABLED', None)
    # plugin enabled by spider_type
    for spider_type in ['auto', 'portia']:
        os.environ['SHUB_SPIDER_TYPE'] = spider_type
        assert _get_enabled_status(settings) == (True, False)
    os.environ['SHUB_SPIDER_TYPE'] = 'other_spider_type'
    assert _get_enabled_status(settings) == (False, False)
    # plugin enabled on error
    settings.set('PAGE_STORAGE_ON_ERROR_ENABLED', True)
    assert _get_enabled_status(settings) == (False, True)


class PageStorageMiddlewareTestCase(TestCase):

    def setUp(self):
        self.spider = Spider('default')
        self.mocked_hsref = mock.Mock()
        self.patch = mock.patch('sh_scrapy.hsref.hsref', self.mocked_hsref)
        self.crawler_mock = mock.Mock()
        self.crawler_mock.settings = Settings(
            {'PAGE_STORAGE_ENABLED': True,
             'PAGE_STORAGE_MODE': 'VERSIONED_CACHE',
             'PAGE_STORAGE_LIMIT': 10,
             'PAGE_STORAGE_ON_ERROR_LIMIT': 5})
        self.mocked_hsref.project.collections.url = '/test/url'
        self.patch.start()
        self.instance = PageStorageMiddleware.from_crawler(self.crawler_mock)

    @mock.patch('sh_scrapy.hsref.hsref')
    def test_from_crawler(self, mocked_hsref):
        crawler_mock = mock.Mock()
        crawler_mock.settings = Settings()
        self.assertRaises(NotConfigured,
                          PageStorageMiddleware.from_crawler,
                          crawler_mock)
        # test creating an instance for all other cases
        crawler_mock.settings = mock.Mock()
        mocked_values = [(True, False), (False, True), (True, True)]
        crawler_mock.settings.side_effect = mocked_values
        for _ in range(len(mocked_values)):
            assert isinstance(PageStorageMiddleware.from_crawler(crawler_mock),
                              PageStorageMiddleware)

    def test_init(self):
        assert self.instance.enabled
        assert not self.instance.on_error_enabled
        assert self.instance.limits == {'all': 10, 'error': 5}
        assert self.instance.counters == {'all': 0, 'error': 0}
        assert self.instance.cookies_seen == set()
        self.mocked_hsref.job.metadata.apipost.assert_called_with(
            'collection', jl='vcs/Pages')
        assert self.instance._writer
        self.mocked_hsref.client.batchuploader.\
            create_writer.assert_called_with(
                '/test/url/vcs/Pages', content_encoding='gzip', size=20)

    def test_process_spider_input(self):
        assert self.instance.counters == {'all': 0, 'error': 0}
        self.instance.save_response = mock.Mock()

        self.instance.process_spider_input('test-response', self.spider)
        assert self.instance.counters == {'all': 1, 'error': 0}

        self.instance.enabled = False
        self.instance.process_spider_input('test-response', self.spider)
        assert self.instance.counters == {'all': 1, 'error': 0}

        self.instance.enabled, self.instance.counters['all'] = True, 11
        self.instance.process_spider_input('test-response', self.spider)
        assert self.instance.counters == {'all': 11, 'error': 0}

        self.instance.limits['all'] = 12
        self.instance.process_spider_input('test-response', self.spider)
        assert self.instance.counters == {'all': 12, 'error': 0}

    def test_process_spider_output(self):
        fake_response = mock.Mock()
        fake_response.request = Request('http://source-request')

        def sort_requests_and_items(val):
            return val.__class__.__name__
        fake_result = sorted([Request('ftp://req1'), Request('https://req2'),
                              Response('http://source-request'), Item(),
                              {'field1': 'value1'}],
                             key=sort_requests_and_items)
        results = self.instance.process_spider_output(
            fake_response, fake_result, self.spider)
        assert isinstance(results, types.GeneratorType)
        for r in sorted(results, key=sort_requests_and_items):
            assert isinstance(r, type(fake_result.pop(0)))
            if isinstance(r, (Item, dict)):
                self.assertEqual(
                    r["_cached_page_id"],
                    request_fingerprint(fake_response.request))
        bad_fake_request = Item()
        bad_fake_request._values = None
        self.instance.process_spider_exception = mock.Mock()
        with self.assertRaises(TypeError):
            for _ in self.instance.process_spider_output(
                    fake_response, [bad_fake_request], self.spider):
                pass
        assert self.instance.process_spider_exception.called

    def test_process_spider_exception(self):
        assert self.instance.counters == {'all': 0, 'error': 0}
        self.instance.save_response = mock.Mock()
        # all conditions are true
        self.instance.on_error_enabled = True
        self.instance.process_spider_exception(
            'err-response', Exception(), self.spider)
        assert self.instance.counters == {'all': 0, 'error': 1}
        # on_error flag is disabled, skipping
        self.instance.on_error_enabled = False
        self.instance.process_spider_exception(
            'err-response', Exception(), self.spider)
        assert self.instance.counters == {'all': 0, 'error': 1}
        # exceeded error limit
        self.instance.on_error_enabled = True
        self.instance.counters['error'] = 11
        self.instance.process_spider_exception(
            'err-response', Exception(), self.spider)
        assert self.instance.counters == {'all': 0, 'error': 11}
        # skip IgnoreRequest
        self.instance.limits['error'] = 12
        self.instance.process_spider_exception(
            'err-response', IgnoreRequest(), self.spider)
        assert self.instance.counters == {'all': 0, 'error': 11}
        # all conditions are true again
        self.instance.limits['all'] = 12
        self.instance.process_spider_exception(
            'err-response', Exception(), self.spider)
        assert self.instance.counters == {'all': 0, 'error': 12}

    def test_save_response(self):
        self.instance._writer = mock.MagicMock()
        self.instance._writer.maxitemsize = 10
        # wrong response type
        self.instance.save_response(
            Response('http://resp', request=Request('http://req')),
            self.spider)
        assert not self.instance._writer.write.called
        # get request with large body
        resp1 = TextResponse('http://resp1',
                             request=Request('http://req1'),
                             body='looong loong body',
                             encoding='cp1251')
        self.instance.save_response(resp1, self.spider)
        assert not self.instance._writer.write.called
        # get request with ok-body
        self.instance.hsref = mock.Mock()
        self.instance.hsref.job.key = '123/45/67'
        resp2 = TextResponse('http://resp2', request=Request('http://req2'),
                             body='body', encoding='cp1251',
                             headers={'Set-Cookie': [b'coo1=test;abc=1',
                                                     b'coo2=tes1;cbd=2']})
        self.instance.save_response(resp2, self.spider)
        self.instance._writer.write.assert_called_with(
            {'body': u'body', '_encoding': 'cp1251', '_type': '_pageitem',
             '_key': 'bad42100b1d34e29973a79e512aabb4db885b712',
             'cookies': ['coo1=test', 'coo2=tes1'],
             'url': 'http://resp2', '_jobid': '123/45/67'})

    def test_save_response_with_trim(self):
        self.instance._writer.maxitemsize = 26
        self.instance.hsref.job.key = '123/45/67'
        resp = TextResponse(
            'http://resp', request=Request('http://req'), encoding='cp1251',
            body='\r\n\r\n<html><body></body></html>\r\n \0\0\0\0\0')
        with mock.patch.object(Spider, 'logger') as log:
            spider = Spider('default')
            self.instance.save_response(resp, self.spider)
        log.warning.assert_called_with(
            "Page not saved, body too large: <http://resp>")
        self.instance.trim_html = True
        self.instance.save_response(resp, spider)
        self.instance._writer.write.assert_called_with(
            {u'body': u'<html><body></body></html>', u'_encoding': u'cp1251',
             u'_type': u'_pageitem',
             u'_key': u'9b4bed7e56103ddf63455ed39145f61f53b3c702',
             u'url': u'http://resp', '_jobid': '123/45/67'})

    def test_save_cookies(self):
        payload = {}
        assert self.instance.cookies_seen == set()
        fake_response = mock.MagicMock()
        self.instance._set_cookies(payload, fake_response)
        assert 'cookies' not in payload

        fake_response.headers.getlist.return_value = [
            b'id=coo2;test=data2;data=test']
        self.instance._set_cookies(payload, fake_response)
        self.assertEqual(payload['cookies'], ['id=coo2'])
        self.assertEqual(self.instance.cookies_seen, set(['id=coo2']))

        fake_response.headers.getlist.return_value = [
            b'id=coo1;test=data',
            b'id=coo2;test=data2;data=test',
            b'id=coo3;coo3=data;test=data']
        self.instance._set_cookies(payload, fake_response)
        self.assertEqual(payload['cookies'], ['id=coo1', 'id=coo3'])
        self.assertEqual(self.instance.cookies_seen,
                         set(['id=coo1', 'id=coo2', 'id=coo3']))

    def test_writer_closed_on_spider_closed_signal(self):
        self.crawler_mock.signals.connect.assert_called_once_with(
            self.instance.spider_closed,
            signal=signals.spider_closed
        )
        with mock.patch.object(self.instance, '_writer') as writer_mock:
            self.instance.spider_closed(self.spider)
        writer_mock.close.assert_called_once_with()

    def tearDown(self):
        self.patch.stop()
