This repository contains a few simple python scripts that collect a
sample of the Twitter firehose and then analyze the URL
shortening/HTTP redirections for links found in those tweets. The
resulting graph shows a histogram of redirects per URL found in
tweets.

Requirements
------------

These scripts use the excellent TweetStream and Requests libraries:

    pip install tweetstream requests

If you want a graph rather than reading raw output, you need
matplotlib as well.

Running
-------

The analysis is a three-step process:

    # Create a JSON-formatted credentials.json file with a single
    # object containing your Twitter 'username' and 'password' to gain
    # access to Twitter's sample stream. Then collect data.
    # This will sync every 100 tweets until you kill it, leaving (a
    # potentially very large) tweets.log file.
    python collect.py

    # Next look for URLs and unwrap them, giving you a json file
    # containing the a list of accessed URLs and status codes for each
    # link found. This will try to follow all the URLs it finds in the
    # tweets. It uses a bunch of threads. Beware of high network IO.
    python unwrap.py

    # Finally, analyze it and generate a few graphs. If you want to
    # generate a different graph, add it somewhere here or just use
    # the redirects.log file generated by the unwrap.py scripts.
    python graph.py

Details
-------

URL detection is a pretty good heuristic, where pretty good means I
logged a bunch of tweets, found URLs manually, and made sure I found
matches with the regex. Some still are missed, some are caught but
catch extra characters (e.g. because extra ')', ':', '"', or random
Unicode characters are appended). I don't have an exact measurement,
but these are small compared to the whole dataset, so they shouldn't
drastically affect the results.

I also required multithreading to get results in a reasonable amount
of time. Many of the links were dead very quickly, and a large
fraction of those were t.co links. I believe these may have been spam
links that Twitter quickly disabled, but I haven't verified that. If
you don't run many concurrent requests, you'll process tweeted links
orders of magnitude slower than you consume them via the sampled
firehose from Twitter.
