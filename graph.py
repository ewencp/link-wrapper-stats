#!/usr/bin/env python

import json, pprint
from operator import itemgetter
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


# Grab the data
with open('redirects.log', 'r') as fp:
    links = json.load(fp)

# Common utilities
def get_domain(url):
    # 'http://www.google.com/foo/bar' => ['http:', '', 'www.google.com', 'foo', 'bar']
    return url.split('/')[2]

def is_shortener_redirect(x):
    # Should be a redirect
    if not (x['status'] == 301 or x['status'] == 302): return False

    # Should be from a shortener. We could encounter regular
    # redirects, e.g. on the site itself. Just look for short
    # domains. This certainly isn't perfect, but it's approximately
    # right. We could filter by known shorteners here if we wanted
    # something more conservative.
    if len(get_domain(x['url'])) > 8: return False

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

bins_ = [x-1 for x in range(10)]
n, bins, patches = plt.hist(redirect_counts, bins_, facecolor='green', align='left', log=True, rwidth=.75)
print "Redirections histogram:"
pprint.pprint(zip(bins, n))

plt.xlabel('# of redirects')
plt.ylabel('# URLs')
plt.title('Histogram of redirects per URL')
plt.grid(True)

plt.savefig('redirects_histogram.png')
#plt.show()



# Figure out top wrappers. Just extract domains and count for each
# redirect found. This is marketshare in some sense.
wrappers = {}
for redirects in links:
    if redirects[-1]["status"] != 200: continue
    # Get just the shortener redirects
    shortener_redirects = [x for x in redirects if is_shortener_redirect(x)]
    # And count
    for rd in shortener_redirects:
        dom = get_domain(rd['url'])
        if dom not in wrappers: wrappers[dom] = 0
        wrappers[dom] += 1
top_wrappers = sorted(wrappers.iteritems(), key=itemgetter(1), reverse=True)[:10]
print "Top URL shorteners:"
pprint.pprint(top_wrappers)

plt.clf()
pos = np.arange(len(top_wrappers))+.5
plt.bar(pos, [x[1] for x in top_wrappers], facecolor='green', align='center', log=True)
plt.xticks(pos, [x[0] for x in top_wrappers], rotation=20)
plt.ylabel('# URLs Shortened')
plt.title('Top URL Shorteners')
plt.grid(True)
plt.savefig('top_shorteners.png')
#plt.show()



# Figure out top rewrappers. Extract domains from URLs and, except for
# the last redirect (the first wrapping), count them up
# per-domain. Unlike the raw count, this indicates who is adding more
# layers of fragility and more latency to links.
rewrappers = {}
for redirects in links:
    if redirects[-1]["status"] != 200: continue
    # Get just the shortener redirects
    shortener_redirects = [x for x in redirects if is_shortener_redirect(x)]
    # Get rewrappers (ignore last one since it's the original short URL for the target)
    for rd in shortener_redirects[:-1]:
        dom = get_domain(rd['url'])
        if dom not in rewrappers: rewrappers[dom] = 0
        rewrappers[dom] += 1
top_rewrappers = sorted(rewrappers.iteritems(), key=itemgetter(1), reverse=True)[:10]
print "Top URL Re-shorteners:"
pprint.pprint(top_rewrappers)

plt.clf()
pos = np.arange(len(top_rewrappers))+.5
plt.bar(pos, [x[1] for x in top_rewrappers], facecolor='green', align='center', log=True)
plt.xticks(pos, [x[0] for x in top_rewrappers], rotation=20)
plt.ylabel('# URLs Re-Shortened')
plt.title('Top URL Re-Shorteners')
plt.grid(True)
plt.savefig('top_reshorteners.png')
#plt.show()
