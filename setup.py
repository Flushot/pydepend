#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Allow trove classifiers in previous python versions
from sys import version as py_version
if py_version < '2.2.3':
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None

from pydepend import __version__ as version

def requireModules(moduleNames=None):
    import re
    if moduleNames is None:
        moduleNames = []
    else:
        moduleNames = moduleNames

    commentPattern = re.compile(r'^\w*?#')
    moduleNames.extend(
        filter(lambda line: not commentPattern.match(line), 
            open('requirements.txt').readlines()))

    return moduleNames

setup(
    name='pydepend',
    version=version,

    author='Chris Lyon',
    author_email='flushot@gmail.com',

    description='Python dependency graph',
    long_description=open('README.md').read(),
    url='https://github.com/Flushot/pydepend',

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers'
    ],

    install_requires=requireModules([

    ]),

    test_suite='pydepend'
)
