#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='dweepy',
    version='0.0.1',
    description='Dweepy is a Python client for dweet.io',
    long_description=open('README.rst').read(),
    author='Patrick Carey',
    author_email='paddy@wackwack.co.uk',
    url='https://github.com/paddycarey/dweepy',
    py_modules=['dweepy'],
    install_requires=['requests >= 2'],
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
    ],
)
