file = open('/Users/nernst/Documents/current-papers/icsm09/data/pickles/Nautilus-Usability.pcl')
n = pickle.load(file)
data = [x[2] for x in n]
n, bins, patches = plt.hist(data, 15)
plt.xlabel('#Events')
plt.ylabel('Frequency')
