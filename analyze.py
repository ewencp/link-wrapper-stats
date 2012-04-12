#!/usr/bin/env python

import json, requests, re
import threading, Queue

def count_redirects(url):
    # Do some extra cleanup that the regex doesn't currently catch
    url = url.rstrip('"):')
    try:
        _r = requests.get(url, timeout=5)
        #if _r.status_code != 200: print url
        return len( [x for x in _r.history if (x.status_code == 301 or x.status_code == 302)] )
    except:
        #print url
        return None

jobs_queue = Queue.Queue()
result_list = []
result_lock = threading.Lock()

class WorkerThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            url = self.queue.get()
            nredirects = count_redirects(url)
            if nredirects is not None:
                result_lock.acquire()
                result_list.append(nredirects)
                if len(result_list) % 100 == 0: print "Processed %d links" % (len(result_list))
                result_lock.release()

            self.queue.task_done()


def normalize_url(url):
    # Simple length heuristic
    if len(url) < 10: return None

    # Make sure we have some sort of protocol
    if not re.search('://', url):
        url = 'http://' + url

    return url

with open('tweets.log', 'rb') as fp:
    count = 0
    url_count = 0

    for i in range(20):
        t = WorkerThread(jobs_queue)
        t.daemon = True
        t.start()

    for line in fp:
        tweet = json.loads(line)

        tweet_text = tweet['text']

        # (Start of line or word)
        # (Maybe something like http://)
        # (A vaguely domain-like section, at least one dot which is not a double dot)
        # (Whatever else follows, liberally via non-whitespace)
        url_regex = '(\A|\\b)([\w-]+://)?\S+[.][^\s.]\S*'

        for sub in tweet_text.split():
            orig_url_match = re.search(url_regex, sub)
            if not orig_url_match:
                continue
            orig_url = normalize_url(orig_url_match.group(0))
            if not orig_url: continue

            url_count += 1
            jobs_queue.put(orig_url)

        count += 1

    # wait on the queue until everything has been processed
    jobs_queue.join()

print "Analyzed %d tweets" % (count)
print "Found %d URLS" % (url_count)
for idx in range(20):
    print "%d => %d" % (idx, len([x for x in result_list if x == idx]) )
