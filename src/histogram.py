import pickle
import numpy as np
import matplotlib.pyplot as plt
file = open('/Users/nernst/Documents/papers/current-papers/refsq/data/pickles/ext/Evolution-Usability.pcl')
n = pickle.load(file)
data = [x[2] for x in n] # where x[2] is the absolute value, not normalized
n, bins, patches = plt.hist(data, bins=15, range=(0,1000))
plt.xlabel('#Events')
plt.ylabel('Frequency')
