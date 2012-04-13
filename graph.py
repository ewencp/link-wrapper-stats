#!/usr/bin/env python

import json

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


# Grab the data
with open('redirects.log', 'r') as fp:
    links = json.load(fp)

# Common utility
def is_shortener_redirect(x):
    # Should be a redirect
    if not (x['status'] == 301 or x['status'] == 302): return False

    # Should be from a shortener. We could encounter regular
    # redirects, e.g. on the site itself. Just look for short
    # domains. This certainly isn't perfect, but it's approximately
    # right. We could filter by known shorteners here if we wanted
    # something more conservative.
    # 'http://www.google.com/foo/bar' => ['http:', '', 'www.google.com', 'foo', 'bar']
    domain = x['url'].split('/')[2]
    if len(domain) > 8: return False

    # And the total length shouldn't be too long either
    if len(x['url']) > 30: return False

    return True




# Generate histogram of number of redirects per link
redirect_counts = []
for redirects in links:
    if redirects[-1]["status"] != 200: continue

    nredirects = len( [x for x in redirects if is_shortener_redirect(x)] )
    redirect_counts.append(nredirects)

print "Analyzed %d links, found %d succesfully loaded" % (len(links), len(redirect_counts))

n, bins, patches = plt.hist(redirect_counts, len(redirect_counts), normed=1, facecolor='green', alpha=0.75)

plt.xlabel('# of redirects')
plt.ylabel('# URLs')
plt.title('Histogram of redirects per URL')
plt.grid(True)

plt.savefig('redirects_histogram.png')
#plt.show()
