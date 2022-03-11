from setuptools import setup

setup(
    name='scrapy-pagestorage',
    version='0.4.0',
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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.5',
    install_requires=[
        'Scrapy>=1.0.3',
        'scrapinghub>=1.9.0',
        'scrapinghub-entrypoint-scrapy>=0.4',
    ],
)
