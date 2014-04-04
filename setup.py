# Copyright (C) 2014 Ivan E. Cao-Berg
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
from setuptools import setup

#load the current version number of the package
exec(compile(open('VERSION').read(),'VERSION', 'exec'))

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name = 'falcon',
      version = __version__,
      description = ('FALCON: '
      	'Feedback Adaptive Loop for Content-Based Retrieval'),
      long_description=read('README.rst'),
      author = 'Ivan Cao-Berg',
      author_email = 'icaoberg@alumni.cmu.edu',
      install_requires=[
      	'numpy',
      	'scipy'],
      url = 'https://github.com/icaoberg/falcon',
      classifiers=[
      	'Programming Language :: Python', 
      	'Intended Audience :: Science/Research',
      	'Intended Audience :: Developers'],
      py_modules=['falcon.search'])
