==================
scrapy-pagestorage
==================

A scrapy extension to store requests and responses information in storage service.

Installation
============

You can install scrapy-pagestorage using pip::

    pip install scrapy-pagestorage

You can then enable the middleware in your `settings.py`::

    SPIDER_MIDDLEWARES = {
        ...
        'scrapy_pagestorage.PageStorageMiddleware': 900
    }

Settings
========

Through `settings.py`::

    PAGE_STORAGE_MODE = "VERSIONED_CACHE"
    PAGE_STORAGE_LIMIT = 100
    PAGE_STORAGE_ON_ERROR_LIMIT = 100


How to use it
=============

TODO
