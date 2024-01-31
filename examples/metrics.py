import urllib.request
import numpy as np
import os
import halcon
from tabulate import tabulate

print(
    """
This example uses the wine dataset from

Machine Learning Repository
Center for Machine Learning and Intelligent Systems
http://archive.ics.uci.edu/ml/datasets/Wine

This example uses this dataset to compare the different metrics available in FALCON
"""
)

url = "http://archive.ics.uci.edu/ml/machine-learning-databases/wine/wine.data"
filename = "data.csv"
urllib.request.urlretrieve(url, filename)
data = np.genfromtxt(filename, delimiter=",")

query_wines = [["wine0", 1, data[0]]]

# metrics
metrics = ["euclidean", "cityblock", "hamming"]

os.remove(filename)

dataset = [
    ["wine" + str(counter), 1, datum] for counter, datum in enumerate(data, start=1)
]

data = {
    metric: halcon.search.query(
        query_wines, dataset, metric=metric, normalization="standard", debug=True
    )[0]
    for metric in metrics
}

table = [
    [index, data["euclidean"][index], data["cityblock"][index], data["hamming"][index]]
    for index in range(20)
]

print(tabulate(table, headers=["Ranking", "Euclidean", "City Block", "Hamming"]))
