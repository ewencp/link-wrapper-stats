#!/usr/bin/env python

import json
import tweetstream
import time, datetime, os

with open('credentials.json', 'r') as fp:
    cred = json.load(fp)

delay = 1
out_fp = open('tweets.log', 'ab')
started = datetime.datetime.now()
while True:
    try:
        count = 0
        with tweetstream.TweetStream(cred["username"], cred["password"]) as stream:
            for tweet in stream:
                # Skip deletions
                if u"delete" in tweet: continue
                # print anything we don't understand
                if not u"user" in tweet or not u"text" in tweet:
                    print tweet
                else:
                    print >>out_fp, "%s\r" % (json.dumps(tweet))
                    count += 1
                    if count % 1000 == 0:
                        out_fp.flush()
                        os.fsync(out_fp.fileno())
                        current = datetime.datetime.now()
                        print "Recorded %d tweets in %s (%f tweets/s)" % (count, str(current-started), float(count)/(current-started).seconds)
    except tweetstream.ConnectionError, e:
        print "Disconnected from twitter. Reason:", e.reason

    # On disconnect, delay. Just do exponential backoff, we don't need
    # enough data to care about anything more complicated (or reducing
    # the timeout)
    time.sleep(delay)
    delay *= 2

out_fp.close()
