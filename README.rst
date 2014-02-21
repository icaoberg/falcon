falcon
======
falcon is a python implementation of FALCON as described in 

* Leejay Wu, Christos Faloutsos, Katia P. Sycara, and Terry R. Payne. 2000. FALCON: Feedback Adaptive Loop for Content-Based Retrieval. In Proceedings of the 26th International Conference on Very Large Data Bases (VLDB '00), Amr El Abbadi, Michael L. Brodie, Sharma Chakravarthy, Umeshwar Dayal, Nabil Kamel, Gunter Schlageter, and Kyu-Young Whang (Eds.). Morgan Kaufmann Publishers Inc., San Francisco, CA, USA, 297-306.

Pre-Requisites
==============
- numpy
- scipy

To install the prerequisites in Ubuntu 12.04
```
sudo apt-get install update
sudo apt-get install python-numpy python-scipy
```

Installation
============
Run
```
sudo python setup.py install
```
 
I have of submitting this package to the Python Package Repository. 
If I do so, then should be able to

``` 
sudo pip install falcon
```

If you wish to install falcon in a virtual enviroment, then you can do
```
virtualenv falcon
cd falcon
source ./bin/activate
pip install numpy
pip install scipy
mkdir src
git clone git@github.com:icaoberg/falcon.git
cd falcon
python setup.py install
cd src
deactivate
```

Documentation
-------------
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

Documentation was written using sphinx.