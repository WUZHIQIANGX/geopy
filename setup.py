#!/usr/bin/env python
"""
geopy
"""

import sys

from setuptools import find_packages, setup

if sys.version_info < (3, 5):
    raise RuntimeError(
        "geopy 2 supports Python 3.5 and above. "
        "Use geopy 1.x if you need Python 2.7 or 3.4 support."
    )

# This import must be below the above `sys.version_info` check,
# because the code being imported here is not compatible with the older
# versions of Python.
from geopy import __version__ as version  # noqa  # isort:skip

INSTALL_REQUIRES = [
    'geographiclib<2,>=1.49',
]

EXTRAS_DEV_TESTFILES_COMMON = [
]

EXTRAS_DEV_LINT = [
    "flake8>=3.6.0,<3.7.0",
    "isort>=4.3.4,<4.4.0",
]

EXTRAS_DEV_TEST = [
    "coverage",
    "pytest>=3.10",
]

EXTRAS_DEV_DOCS = [
    "readme_renderer",
    "sphinx",
    "sphinx_rtd_theme>=0.4.0",
]

setup(
    name='geopy',
    version=version,
    description='Python Geocoding Toolbox',
    long_description=open('README.rst').read(),
    author='GeoPy Contributors',
    author_email='uijllji@gmail.com',
    url='https://github.com/geopy/geopy',
    download_url=(
        'https://github.com/geopy/geopy/archive/%s.tar.gz' % version
    ),
    packages=find_packages(exclude=["*test*"]),
    install_requires=INSTALL_REQUIRES,
    extras_require={
        "dev": (EXTRAS_DEV_TESTFILES_COMMON +
                EXTRAS_DEV_LINT +
                EXTRAS_DEV_TEST +
                EXTRAS_DEV_DOCS),
        "dev-lint": (EXTRAS_DEV_TESTFILES_COMMON +
                     EXTRAS_DEV_LINT),
        "dev-test": (EXTRAS_DEV_TESTFILES_COMMON +
                     EXTRAS_DEV_TEST),
        "dev-docs": EXTRAS_DEV_DOCS,
        "requests": ["requests"],
        "timezone": ["pytz"],
    },
    license='MIT',
    keywords='geocode geocoding gis geographical maps earth distance',
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ]
)
