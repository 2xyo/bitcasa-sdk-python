# -*- coding: utf-8 -*-
import os
import sys

import bitcasa

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
    name=bitcasa.__title__,
    version=bitcasa.__version__,
    author=bitcasa.__author__,
    author_email='api@bitcasa.com',
    maintainer=bitcasa.__author__,
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
    license=bitcasa.__license__,
    keywords='bitcasa sdk',
    packages=[bitcasa.__title__, '{0}.tests'.format(bitcasa.__title__)],
    package_data={bitcasa.__title__: ['../testing.ini',
                                 '../README.rst',
                                 '../LICENSE']},
    install_requires=['requests>=1.2.3', 'nose', 'nose-testconfig'],
    entry_points={},
    test_suite='{0}.tests'.format(bitcasa.__title__))
