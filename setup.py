#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='dweepy',
    version='0.3.0',
    description='Dweepy is a Python client for dweet.io',
    long_description=open('README.rst').read(),
    author='Patrick Carey',
    author_email='paddy@wackwack.co.uk',
    url='https://github.com/paddycarey/dweepy',
    packages=[
        'dweepy',
    ],
    package_dir={'dweepy':
                 'dweepy'},
    include_package_data=True,
    install_requires=['requests >= 2, < 3'],
    license="MIT",
    zip_safe=False,
    keywords='dweepy dweet dweet.io',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    test_suite='tests_dweepy',
)
