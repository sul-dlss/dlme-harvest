#!/usr/bin/python
import feedparser, io, json, os

urls = { 'persian': 'http://shahrefarang.com/feed/',
         'english': 'http://shahrefarang.com/en/feed/',
         'arabic': 'http://shahrefarang.com/ar/feed/'}

for key, value in urls.items():
    count = 1
    for i in range(12):
        url = "{}?paged={}".format(value, i)
        feed = feedparser.parse(url)
        for post in feed.entries:
            filename = 'output/shahre-farang/{}/data/{}-{}.json'.format(key, key, count)
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with io.open(filename, 'w') as out_file:
                out_file.write(json.dumps(post))
            count += 1
