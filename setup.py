# -*- coding: utf-8 -*-
import os
import re
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

PACKAGE_NAME = 'bitcasa'

HERE = os.path.abspath(os.path.dirname(__file__))
INIT = open(os.path.join(HERE, PACKAGE_NAME, '__init__.py')).read()
README = open(os.path.join(HERE, 'README.md')).read()

VERSION = re.search("__version__ = '([^']+)'", INIT).group(1)

with open('README.md') as f:
    readme = f.read()

with open('LICENSE.txt') as f:
    license = f.read()

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author='Bitcasa, Inc.',
    author_email='api@bitcasa.com',
    maintainer='Bitcasa, Inc.',
    maintainer_email='api@bitcasa.com',
    url='http://www.bitcasa.com/',
    description=('This is the Python SDK for the Bitcasa API.'),
    long_description=README,
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Environment :: Web Environment',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.1',
                 'Programming Language :: Python :: 3.2',
                 'Programming Language :: Python :: 3.3',
                 'Topic :: Utilities'],
    license='MIT',
    keywords='bitcasa sdk',
    packages=[PACKAGE_NAME, '{0}.tests'.format(PACKAGE_NAME)],
    package_data={'': ['COPYING'], PACKAGE_NAME: ['*.ini']},
    install_requires=['requests>=1.2.3','nose','nose-testconfig'],
    entry_points={},
    test_suite='{0}.tests'.format(PACKAGE_NAME))
