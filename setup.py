import os
from setuptools import setup, find_packages

__version__ = '1.1'

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='halcon',
    version=__version__,
    description='Python implementation of FALCON: Feedback Adaptive Loop for Content-Based Retrieval',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    author='Ivan E. Cao-Berg',
    author_email='icaoberg@alumni.cmu.edu',
    install_requires=[
        'mpmath==1.3.0',
        'numpy==1.26.3',
        'scipy==1.12.0',
        'setuptools==68.2.2',
        'tabulate==0.9.0',
        'urllib3==1.26.18'
    ],
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
        'Development Status :: 4 - Beta'
    ],
    packages=find_packages(),  # Automatically find all packages and subpackages
    include_package_data=True,  # Include non-python files
    py_modules=['halcon.search'], 
    python_requires='>=3.6',
    tests_require=["nose"]
)
