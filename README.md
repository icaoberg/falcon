halcon
======

[![GitHub issues](https://img.shields.io/github/issues/icaoberg/falcon.svg)](https://github.com/icaoberg/falcon/issues)
[![GitHub forks](https://img.shields.io/github/forks/icaoberg/falcon.svg)](https://github.com/icaoberg/falcon/network)
[![GitHub stars](https://img.shields.io/github/stars/icaoberg/falcon.svg)](https://github.com/icaoberg/falcon/stargazers)
[![GitHub license](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://raw.githubusercontent.com/icaoberg/falcon/master/LICENSE)
[![Twitter](https://img.shields.io/twitter/url/https/github.com/icaoberg/falcon.svg?style=social)](https://twitter.com/intent/tweet?text=Wow:&url=%5Bobject%20Object%5D)

halcon is a python implementation of the Feedback Adaptive Loop for Content-Based Retrieval (FALCON) algorithm as described in 

* Leejay Wu, Christos Faloutsos, Katia P. Sycara, and Terry R. Payne. 2000. FALCON: Feedback Adaptive Loop for Content-Based Retrieval. In Proceedings of the 26th International Conference on Very Large Data Bases (VLDB '00), Amr El Abbadi, Michael L. Brodie, Sharma Chakravarthy, Umeshwar Dayal, Nabil Kamel, Gunter Schlageter, and Kyu-Young Whang (Eds.). Morgan Kaufmann Publishers Inc., San Francisco, CA, USA, 297-306.
 
FALCON is, as described in the article abstract, "a novel method that is designed to handle disjunctive queries within metric spaces. The user provides weights for positive examples; our system 'learns' the implied concept and returns similar objects."

### Development branch status
[![Build Status](https://travis-ci.org/icaoberg/falcon.svg?branch=dev)](https://travis-ci.org/icaoberg/falcon)

### Master branch status
[![Build Status](https://travis-ci.org/icaoberg/falcon.svg?branch=master)](https://travis-ci.org/icaoberg/falcon)

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

There are several ways to install halcon. The most common way is to download the source code, unzip/untar the source code package and run the command

```
sudo python setup.py install
```
 
I have plans of submitting this package to the Python Package Index. 
If I do so, then should be able to install it by running the command

```
sudo pip install halcon
```

**COMMENT**: halcon depends on [numpy](http://www.numpy.org) and [scipy](http://www.scipy.org). Installing these packages in Windows and MacOSX is not a trivial task. For more information refer to the documentation.

If you wish to install halcon in a virtual enviroment, then you can do

```
virtualenv halcon
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

Usage
-----
There is only one method that you need to know about

```
halcon.search.query(good_set, candidates, alpha=-5, 
        metric='euclidean', normalization='zscore', debug=False)
```

Here is a brief description of each of the input arguments 

* ```good_set``` and ```candidates``` are two lists of lists where each member of both lists has the same shape.

  ```
  record = [ <identifier>, <initial_score>, <feature_vector>]
  ```

  For example in ```wine.py```, I download a CSV file where the first ```feature_vector``` looks like this

  ```
  1,14.23,1.71,2.43,15.6,127,2.8,3.06,.28,2.29,5.64,1.04,3.92,1065
  ```

  and then I modify it like this

  ```
  good_set = []
  identifier = 'wine00'
  initial_score = 1
  feature_vector = [1,14.23,1.71,2.43,15.6,127,2.8,3.06,.28,2.29,5.64,1.04,3.92,1065]
  good_set.append([identifier, initial_score, feature_vector])
  ```

  For more information about the definition of the initial score, please refer to the article. In all my examples I use a initial score of 1, that is, all images have the same weight. The identifier should be unique (though not enforced), so you can tell images apart. This package assumes every object is represented by a [feature](http://en.wikipedia.org/wiki/Feature_(machine_learning)) vector. Feature calculation goes beyond the scope of this package. There are many feature calculation/machine learning packages out there that you might find useful, like [OpenCV](http://opencv.org/), [mahotas](https://pypi.python.org/pypi/mahotas) and [SLIC](http://lanec1web1.compbio.cs.cmu.edu/release/).

* ```alpha```. For more information about alpha, please refer to the article. The recommended value by the paper is -5, which is the default value used in this package.

* ```metric```. In the research article, a measure of distance ```d``` is used to calculate the distance between two feature vectors. The default value is ```euclidean``` (Euclidean distance) and other supported metrics are ```cityblock``` (Manhattan distance) and ```hamming``` (Hamming distance).

* ```normalization```. Feature normalization option. Default is ```zscore```. Alternative option is ```standard```.

* ```debug```. If debug flag is on, then it should print more information about the calculation as they happen. 

Examples
--------
For convenience and testing I included some examples. These examples download some
datasets from the web and use them to trigger a query. The only exception is the random feature vectors example. For example, to run the ```iris``` example simply run in terminal

```
python examples/iris.py
```

The examples have a dependency that the package does not, since I use [tabulate](https://pypi.python.org/pypi/tabulate) to pretty print the results from the examples.

In my humble opinion, the best way to run the examples is using [virtualenv](https://pypi.python.org/pypi/virtualenv) -which is what I do for [travis](https://travis-ci.org/icaoberg/falcon)-. The next commands assume you have virtualenv available.

```
virtualenv halcon --system-site-packages
. ./falcon/bin/activate
cd falcon
mkdir src
cd src
pip install numpy
pip install scipy
pip install tabulate
git clone https://github.com/icaoberg/falcon.git
cd falcon
python setup.py install
cd ..
python examples/iris.py
```

### iris.py

```
$ python examples/iris.py
This example uses the iris dataset from
Machine Learning Repository
Center for Machine Learning and Intelligent Systems
http://archive.ics.uci.edu/ml/datasets/Iris
I will use the first feature vector as my query image
[[0, 1, array([ 5.1,  3.5,  1.4,  0.2,  1. ])]]
And I will use the rest of the feature vectors to find the most similar images
Now notice that feature vector with iid1 has the same values iid0
[1, 1, array([ 5.1,  3.5,  1.4,  0.2,  1. ])]
So I expect that if FALCON is working correctly, then iid1 should be the top hit!
Elapsed time: 0.0221660137177 seconds

  Ranking    Identifier  Class                  Score
---------  ------------  ---------------  -----------
        0             1  Iris-setosa      0
        1            28  Iris-setosa      1.27788e-43
        2             5  Iris-setosa      2.40121e-40
        3            29  Iris-setosa      2.40121e-40
        4            40  Iris-setosa      5.83391e-40
        5             8  Iris-setosa      7.04398e-39
        6            18  Iris-setosa      1.1259e-35
        7            41  Iris-setosa      1.51906e-34
        8            50  Iris-versicolor  6.99696e-34
        9            37  Iris-setosa      1.09221e-32
       10            12  Iris-setosa      1.22203e-32
       11            49  Iris-setosa      2.05046e-32
       12            11  Iris-setosa      4.25801e-31
       13            21  Iris-setosa      6.55842e-31
       14            47  Iris-setosa      5.54098e-29
       15            36  Iris-setosa      7.93943e-29
       16             7  Iris-setosa      2.16985e-28
       17            20  Iris-setosa      4.23544e-28
       18            25  Iris-setosa      1.67453e-27
       19             3  Iris-setosa      2.40919e-27
Do the top results in the list above belong to the same class as the query image?
If so, then SCORE! It seems to work.
```

### wine.py

```
$ python examples/wine.py
This example uses the wine dataset from
Machine Learning Repository
Center for Machine Learning and Intelligent Systems
http://archive.ics.uci.edu/ml/datasets/Wine
I will use the first three feature vectors as my query wine set
And I will use the rest of the feature vectors to find the most similar images
Elapsed time: 0.0280928611755 seconds

  Ranking  Identifier          Score
---------  ------------  -----------
        0  wine1         0
        1  wine2         0
        2  wine3         0
        3  wine21        2.77663e-05
        4  wine30        0.000629879
        5  wine23        0.00252617
        6  wine49        0.00318536
        7  wine57        0.00456123
        8  wine36        0.0152067
        9  wine39        0.0197516
       10  wine58        0.0243848
       11  wine9         0.024467
       12  wine55        0.045762
       13  wine24        0.046893
       14  wine7         0.113906
       15  wine45        0.188355
       16  wine27        0.201802
       17  wine41        0.206469
       18  wine31        0.288536
       19  wine56        0.291853
```

### metrics.py

```
$ python examples/metrics.py
This example uses the wine dataset from
Machine Learning Repository
Center for Machine Learning and Intelligent Systems
http://archive.ics.uci.edu/ml/datasets/Wine
This example uses this dataset to compare the different metrics available in FALCON

  Ranking  Euclidean    City Block    Hamming
---------  -----------  ------------  ---------
        0  wine1        wine1         wine1
        1  wine21       wine21        wine5
        2  wine57       wine57        wine47
        3  wine41       wine23        wine3
        4  wine23       wine30        wine9
        5  wine30       wine41        wine17
        6  wine45       wine49        wine25
        7  wine10       wine55        wine30
        8  wine48       wine9         wine36
        9  wine7        wine7         wine39
       10  wine36       wine36        wine41
       11  wine55       wine10        wine45
       12  wine56       wine45        wine52
       13  wine52       wine56        wine2
       14  wine3        wine48        wine4
       15  wine43       wine47        wine6
       16  wine9        wine52        wine7
       17  wine49       wine3         wine8
       18  wine29       wine17        wine10
       19  wine8        wine8         wine11
```

COMMENT: Hamming distance is meant for comparing strings so this example does not make a lot of sense since these features do not represent characters.

### random_feature_vectors.py

```
$ python examples/random_feature_vectors.py
Generating random query image
Query image name: img
Elapsed time: 7.39097595215e-05 seconds
Generating random dataset
Elapsed time: 0.00141191482544 seconds
Querying with one image
Elapsed time: 0.0233750343323 seconds
Top Ten Results!
  Ranking  Identifier          Score
---------  ------------  -----------
        0  img           0
        1  8             1.30582e+14
        2  85            2.70987e+14
        3  25            3.68567e+14
        4  97            6.19091e+14
        5  11            6.54178e+14
        6  70            6.55048e+14
        7  91            6.89901e+14
        8  79            7.17429e+14
```

### number_of_feature_vectors_performance-euclidean_distance.py

```
$ python examples/number_of_feature_vectors_performance-euclidean_distance.py
Generating and querying on synthetic datasets, please wait...

These are the results from this test
  Number of Feature Vectors    Time (in seconds)
---------------------------  -------------------
                        100            0.0247221
                        200            0.0378191
                        300            0.0665781
                        400            0.0999439
                        500            0.123964
                        600            0.120883
                        700            0.138576
                        800            0.176096
                        900            0.180116

There is a clear trend that is dependent on the number of feature vectors. You know what? Why don't we try making a pretty plot as well
```

![](https://raw.githubusercontent.com/icaoberg/falcon/master/images/number_of_feature_vectors_performance-euclidean_distance.png)

COMMENT: the examples are not seeded so you might get different results.

### number_of_features_performance-euclidean_distance.py

``` 
$ python examples/number_of_features_performance-euclidean_distance.py
Generating and querying on synthetic datasets, please wait...                   ]

These are the results from this test

  Number of Features    Time (in seconds)
--------------------  -------------------
                  50            0.0666399
                 100            0.0619891
                 150            0.0683651
                 200            0.0779331
                 250            0.077204
                 300            0.0829229
                 350            0.087312
                 400            0.092144
                 450            0.09745
                 500            0.111081
                 550            0.112051
                 600            0.11652
                 650            0.119202
                 700            0.123624
                 750            0.127126
                 800            0.134157
                 850            0.138586
                 900            0.149411
                 950            0.14823

There is a clear trend that is dependent on the number of feature vectors. You know what? Why don't we try making a pretty plot as well
```

![](https://raw.githubusercontent.com/icaoberg/falcon/dev/images/number_of_feature_performance-euclidean_distance.png)

COMMENT: the examples are not seeded so you might get different results.

### alphas.py

```
$ python examples/alphas.py
This example uses the wine dataset from
Machine Learning Repository
Center for Machine Learning and Intelligent Systems
http://archive.ics.uci.edu/ml/datasets/Wine
This example uses this dataset to compare results at different alphas

  Ranking  alpha:-100    alpha:-50    alpha:-5    alpha:5    alpha:50    alpha:100
---------  ------------  -----------  ----------  ---------  ----------  -----------
        0  wine1         wine1        wine1       wine1      wine1       wine1
        1  wine2         wine2        wine21      wine21     wine2       wine2
        2  wine3         wine3        wine57      wine57     wine3       wine3
        3  wine4         wine4        wine41      wine41     wine4       wine4
        4  wine5         wine5        wine23      wine23     wine5       wine5
        5  wine6         wine6        wine30      wine30     wine6       wine6
        6  wine7         wine7        wine45      wine45     wine7       wine7
        7  wine8         wine8        wine10      wine10     wine8       wine8
        8  wine9         wine9        wine48      wine48     wine9       wine9
        9  wine10        wine10       wine7       wine7      wine10      wine10
       10  wine11        wine11       wine36      wine36     wine11      wine11
       11  wine12        wine12       wine55      wine55     wine12      wine12
       12  wine13        wine13       wine56      wine56     wine13      wine13
       13  wine14        wine14       wine52      wine52     wine14      wine14
       14  wine15        wine15       wine3       wine3      wine15      wine15
       15  wine16        wine16       wine43      wine43     wine16      wine16
       16  wine17        wine17       wine9       wine9      wine17      wine17
       17  wine18        wine18       wine49      wine49     wine18      wine18
       18  wine19        wine19       wine29      wine29     wine19      wine19
       19  wine20        wine20       wine8       wine8      wine20      wine20
       20  wine21        wine21       wine25      wine25     wine21      wine21
       21  wine22        wine22       wine50      wine50     wine22      wine22
       22  wine23        wine23       wine24      wine24     wine23      wine23
       23  wine24        wine24       wine27      wine27     wine24      wine24
       24  wine25        wine25       wine58      wine58     wine25      wine25
       25  wine26        wine26       wine47      wine47     wine26      wine26
       26  wine27        wine27       wine20      wine20     wine27      wine27
       27  wine28        wine28       wine11      wine11     wine28      wine28
       28  wine29        wine29       wine17      wine17     wine29      wine29
       29  wine30        wine30       wine53      wine53     wine30      wine30
       30  wine31        wine31       wine13      wine13     wine31      wine31
       31  wine32        wine32       wine2       wine2      wine32      wine32
       32  wine33        wine33       wine6       wine6      wine33      wine33
       33  wine34        wine34       wine54      wine54     wine34      wine34
       34  wine35        wine35       wine35      wine35     wine35      wine35
       35  wine36        wine36       wine59      wine59     wine36      wine36
       36  wine37        wine37       wine33      wine33     wine37      wine37
       37  wine38        wine38       wine32      wine32     wine38      wine38
       38  wine39        wine39       wine16      wine16     wine39      wine39
       39  wine40        wine40       wine31      wine31     wine40      wine40
       40  wine41        wine41       wine4       wine4      wine41      wine41
       41  wine42        wine42       wine37      wine37     wine42      wine42
       42  wine43        wine43       wine18      wine18     wine43      wine43
       43  wine44        wine44       wine51      wine51     wine44      wine44
       44  wine45        wine45       wine12      wine12     wine45      wine45
       45  wine46        wine46       wine40      wine40     wine46      wine46
       46  wine47        wine47       wine5       wine5      wine47      wine47
       47  wine48        wine48       wine39      wine39     wine48      wine48
       48  wine49        wine49       wine22      wine22     wine49      wine49
       49  wine50        wine50       wine38      wine38     wine50      wine50
       50  wine51        wine51       wine15      wine15     wine51      wine51
       51  wine52        wine52       wine14      wine14     wine52      wine52
       52  wine53        wine53       wine28      wine28     wine53      wine53
       53  wine54        wine54       wine34      wine34     wine54      wine54
       54  wine55        wine55       wine46      wine46     wine55      wine55
       55  wine56        wine56       wine42      wine42     wine56      wine56
       56  wine57        wine57       wine26      wine26     wine57      wine57
       57  wine58        wine58       wine110     wine110    wine58      wine58
       58  wine59        wine59       wine19      wine19     wine59      wine59
       59  wine63        wine64       wine44      wine44     wine64      wine63
       60  wine64        wine66       wine82      wine82     wine66      wine64
       61  wine66        wine67       wine121     wine121    wine67      wine66
       62  wine67        wine74       wine67      wine67     wine74      wine67
       63  wine68        wine75       wine75      wine75     wine75      wine68
       64  wine70        wine79       wine99      wine99     wine79      wine70
       65  wine72        wine82       wine66      wine66     wine82      wine72
       66  wine73        wine85       wine74      wine74     wine85      wine73
       67  wine74        wine86       wine96      wine96     wine86      wine74
       68  wine75        wine96       wine105     wine105    wine96      wine75
       69  wine77        wine98       wine85      wine85     wine98      wine77
       70  wine79        wine99       wine101     wine101    wine99      wine79
       71  wine80        wine101      wine64      wine64     wine101     wine80
       72  wine81        wine105      wine79      wine79     wine105     wine81
       73  wine82        wine110      wine86      wine86     wine110     wine82
       74  wine83        wine121      wine98      wine98     wine121     wine83
       75  wine85        wine103      wine103     wine103    wine103     wine85
       76  wine86        wine72       wine72      wine72     wine72      wine86
       77  wine87        wine95       wine95      wine95     wine95      wine87
       78  wine88        wine94       wine94      wine94     wine94      wine88
       79  wine89        wine70       wine70      wine70     wine70      wine89
       80  wine90        wine107      wine107     wine107    wine107     wine90
       81  wine94        wine127      wine127     wine127    wine127     wine94
       82  wine95        wine126      wine126     wine126    wine126     wine95
       83  wine96        wine68       wine68      wine68     wine68      wine96
       84  wine97        wine109      wine109     wine109    wine109     wine97
       85  wine98        wine118      wine118     wine118    wine118     wine98
       86  wine99        wine117      wine117     wine117    wine117     wine99
       87  wine100       wine80       wine80      wine80     wine80      wine100
       88  wine101       wine100      wine100     wine100    wine100     wine101
       89  wine102       wine81       wine81      wine81     wine81      wine102
       90  wine103       wine77       wine77      wine77     wine77      wine103
       91  wine104       wine129      wine129     wine129    wine129     wine104
       92  wine105       wine115      wine115     wine115    wine115     wine105
       93  wine107       wine63       wine63      wine63     wine63      wine107
       94  wine109       wine112      wine112     wine112    wine112     wine109
       95  wine110       wine120      wine120     wine120    wine120     wine110
       96  wine111       wine73       wine73      wine73     wine73      wine111
       97  wine112       wine89       wine89      wine89     wine89      wine112
       98  wine114       wine111      wine111     wine111    wine111     wine114
       99  wine115       wine125      wine125     wine125    wine125     wine115
```

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

Bugs and Questions
------------------
To submit bugs about the source code visit

https://github.com/icaoberg/falcon

To submit bugs about the documentation visit

https://github.com/icaoberg/falcon-docs

For any other inquiries visit those links as well.
