from setuptools import setup, find_packages

setup(
    name='scrapy-pagestorage',
    version='0.0.1',
    url='https://github.com/scrapy-plugins/scrapy-pagestorage',
    description='Scrapy extension to store info in storage service',
    long_description=open('README.rst').read(),
    author='Scrapy developers',
    license='BSD',
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
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
    requires=['scrapy (>=1.0.3)'],
)
