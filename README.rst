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

How to use it
=============

Enable extension through `settings.py`::

    PAGE_STORAGE_ENABLED = True
    PAGE_STORAGE_ON_ERROR_ENABLED = True

Configure the exension through `settings.py`::

    PAGE_STORAGE_MODE = "VERSIONED_CACHE"
    PAGE_STORAGE_LIMIT = 100
    PAGE_STORAGE_ON_ERROR_LIMIT = 100

The extension is auto-enabled for auto-spiders (`SHUB_SPIDER_TYPE` in [`auto`, `portia`]).

Settings
========

PAGE_STORAGE_MODE
-----------------
Default: ``None``

A string which specifies if the extension will store information using cache store or
versioned cache store (set `PAGE_STORAGE_MODE="VERSIONED_CACHE"` to use versioned one).

PAGE_STORAGE_LIMIT
------------------
An integer to set a limit of visited pages amount to store.

PAGE_STORAGE_ON_ERROR_LIMIT
---------------------------
An integer to set a limit for page errors amount to store.
