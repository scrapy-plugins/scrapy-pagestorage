from setuptools import setup

setup(
    name='scrapy-pagestorage',
    version='0.0.1',
    url='https://github.com/scrapy-plugins/scrapy-pagestorage',
    description='Scrapy extension to store info in storage service',
    long_description=open('README.rst').read(),
    author='Scrapy developers',
    license='BSD',
    py_modules=['scrapy_pagestorage'],
    zip_safe=False,
    author_email='opensource@scrapinghub.com',
    platforms=['Any'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    requires=['Scrapy (>=1.0.3)'],
    install_requires=[
        'scrapinghub-entrypoint-scrapy==0.4'
    ],
    dependency_links=[
        'http://github.com/scrapinghub/scrapinghub-entrypoint-scrapy/'
        'tarball/0.4#egg=scrapinghub-entrypoint-scrapy',
    ],
)
