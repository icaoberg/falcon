import urllib3
import shutil
from numpy import genfromtxt
from os import remove
from halcon import search
from time import time
from sys import exit
from tabulate import tabulate

print(
    """
This example uses the Iris dataset from

Machine Learning Repository
Center for Machine Learning and Intelligent Systems
http://archive.ics.uci.edu/ml/datasets/Iris
"""
)

url = "http://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
filename = "iris.csv"

http = urllib3.PoolManager()
with open(filename, "wb") as out:
    r = http.request("GET", url, preload_content=False)
    shutil.copyfileobj(r, out)

data = genfromtxt(filename, delimiter=",")

infile = open(filename)
outfile = open("iris2.csv", "w")

replacements = {"Iris-virginica": "0", "Iris-setosa": "1", "Iris-versicolor": "2"}

for line in infile:
    for src, target in replacements.items():
        line = line.replace(src, target)
    outfile.write(line)
infile.close()
outfile.close()

remove(filename)
filename = "iris2.csv"
data = genfromtxt(filename, delimiter=",")

print("I will use the first feature vector as my query image")
query_image = [[0, 1, data[0]]]
print(query_image)

print(
    "\nAnd I will use the rest of the feature vectors"
    + " to find the most similar images"
)
dataset = []
counter = 1
for datum in data:
    dataset.append([counter, 1, datum])
    counter = counter + 1

print("\nNow notice that feature vector with iid1 has the same values iid0")
print(dataset[0])

print(
    "\nSo I expect that if FALCON is working correctly,"
    + " then iid1 should be the top hit!"
)

t = time()
[iids, scores] = search.query(query_image, dataset, normalization="standard")
t = time() - t
print("Elapsed time: " + str(t) + " seconds\n")

iids = iids[0:20]
scores = scores[0:20]

rank = 0
table = []

for index in range(len(iids)):
    iclass = dataset[iids[index]][2][-1]
    if iclass == 0.0:
        iclass = "Iris-virginica"
    elif iclass == 1.0:
        iclass = "Iris-setosa"
    else:
        iclass = "Iris-versicolor"

    table.append([str(rank), str(iids[index]), iclass, str(scores[index])])
    rank = rank + 1

print(tabulate(table, headers=["Ranking", "Identifier", "Class", "Score"]))

print(
    "\nDo the top results in the list above belong to the "
    + "same class as the query image?"
)
print("If so, then SCORE! It seems to work.")

remove("iris2.csv")
