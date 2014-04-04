falcon
======
falcon is a python implementation of the eedback Adaptive Loop for Content-Based Retrieval (FALCON) algorith as described in 

* Leejay Wu, Christos Faloutsos, Katia P. Sycara, and Terry R. Payne. 2000. FALCON: Feedback Adaptive Loop for Content-Based Retrieval. In Proceedings of the 26th International Conference on Very Large Data Bases (VLDB '00), Amr El Abbadi, Michael L. Brodie, Sharma Chakravarthy, Umeshwar Dayal, Nabil Kamel, Gunter Schlageter, and Kyu-Young Whang (Eds.). Morgan Kaufmann Publishers Inc., San Francisco, CA, USA, 297-306.
 
FALCON is, as described in the article abstract, "a novel method that is designed to handle disjunctive queries within metric spaces. The user provides weights for positive examples; our system 'learns' the implied concept and returns similar objects."

Development branch status
-------------------------
[![Build Status](https://travis-ci.org/icaoberg/falcon.svg?branch=dev)](https://travis-ci.org/icaoberg/falcon)

Pre-Requisites
--------------
- numpy
- scipy

To install the prerequisites in Ubuntu 12.04

```
sudo apt-get install update
sudo apt-get install python-numpy python-scipy
```

Installation
============

There are several ways to install falcon. The most common way is to download the source code, unzip/untar the source code package and run the command
```
sudo python setup.py install
```
 
I have plans of submitting this package to the Python Package Index. 
If I do so, then should be able to install it by running the command

```
sudo pip install falcon
```

**COMMENT**: falcon depends on [numpy](http://www.numpy.org) and [scipy](http://www.scipy.org). Installing these packages in Windows and MacOSX is not a trivial task. For more information refer to the documentation.

If you wish to install falcon in a virtual enviroment, then you can do

```
virtualenv falcon
cd falcon
source ./bin/activate
pip install numpy
pip install scipy
mkdir src
cd src
git clone git@github.com:icaoberg/falcon.git
cd falcon
python setup.py install
cd ../../
deactivate
```

**COMMENT**: The previous snippet assumes that you have [virtualenv](https://pypi.python.org/pypi/virtualenv) installed in your working system.

Documentation
-------------
Documentation was written using [Sphinx](http://sphinx-doc.org/).
 To generate documentation use the following commands.

To generate html
```
cd docs
make html
```

To generate PDF document
```
cd docs
make latexpdf
```

To generate epub document
```
cd docs
make epub
```
