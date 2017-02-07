from setuptools import setup

setup(
    name='scrapy-pagestorage',
    version='0.2.0',
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
    install_requires=[
        'Scrapy>=1.0.3',
        'scrapinghub>=1.9.0',
        'scrapinghub-entrypoint-scrapy>=0.4',
    ],
    dependency_links=[
        'git+https://github.com/scrapinghub/scrapinghub-entrypoint-scrapy.git@0.4#egg=scrapinghub_entrypoint_scrapy-0.4',   # noqa
    ],
)
