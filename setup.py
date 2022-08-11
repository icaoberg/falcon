# Copyright (C) 2014-2022 Ivan E. Cao-Berg
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation; either version 2 of the License,
# or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

import os
from setuptools import setup, find_packages

#load the current version number of the package
exec(compile(open('VERSION').read(), 'VERSION', 'exec'))

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name = 'halcon',
      version = __version__,
      description = ('Python implementation of FALCON: '
      	'Feedback Adaptive Loop for Content-Based Retrieval'),
      long_description=read('README.md'),
      long_description_content_type="text/markdown",
      author = 'Ivan E. Cao-Berg',
      author_email = 'icaoberg@alumni.cmu.edu',
      install_requires=[
            'numpy',
            'scipy',
            'mpmath'],
      project_urls={
        'Bug Tracker': 'https://github.com/icaoberg/falcon',
        'Documentation': 'https://github.com/icaoberg/falcon-docs',
        'Source Code': 'https://github.com/icaoberg/falcon',
      },
      classifiers=[
      	'Programming Language :: Python :: 3',
      	'Intended Audience :: Science/Research',
            'Intended Audience :: Developers',
            'Intended Audience :: Information Technology',
            'Topic :: Scientific/Engineering :: Bio-Informatics',
            'Topic :: Scientific/Engineering :: Information Analysis',
            'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
            'Operating System :: OS Independent',
            'Development Status :: 5 - Production/Stable'],
      py_modules=['halcon.search'],
      python_requires='>=3.6',
      tests_require=["nose"]
)
