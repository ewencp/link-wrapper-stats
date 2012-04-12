#!/usr/bin/env python

hist = [0] * 20
with open('results.log', 'r') as fp:
    for line in fp:
        parts = line.split('=>')
        if len(parts) != 2: continue
        idx, count = int(parts[0]), int(parts[1])
        hist[idx] = count

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

# the histogram of the data. seems easiest to undo the histogram we
# already have to get matplotlib to generate a nice graph
data = []
for x in range(20):
    for z in range(hist[x]):
        data.append(x)
n, bins, patches = plt.hist(data, len(hist), normed=1, facecolor='green', alpha=0.75)

plt.xlabel('# of redirects')
plt.ylabel('Fraction of URLs')
plt.title('Histogram of redirects per URL')
plt.grid(True)

plt.show()
