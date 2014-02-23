# -*- coding: utf-8 -*-
import os
import sys

execfile('bitcasa/version.py')

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

with open('README.rst') as f:
    README = f.read()

setup(
    name=__title__,
    version=__version__,
    author=__author__,
    author_email='api@bitcasa.com',
    maintainer=__author__,
    maintainer_email='api@bitcasa.com',
    url='http://www.bitcasa.com/',
    download_url='https://github.com/bitcasa/bitcasa-sdk-python/tarball/v1.0',
    description=('This is the Python SDK for the Bitcasa API.'),
    long_description=README,
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Environment :: Web Environment',
                 'Natural Language :: English',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.2',
                 'Programming Language :: Python :: 3.3',
                 'Topic :: Utilities'],
    license=__license__,
    keywords='bitcasa sdk',
    packages=[__title__, '{0}.tests'.format(__title__)],
    package_data={__title__: ['../testing.ini',
                                 '../README.rst',
                                 '../LICENSE']},
    install_requires=['requests>=1.2.3', 'nose', 'nose-testconfig'],
    entry_points={},
    test_suite='{0}.tests'.format(__title__))
