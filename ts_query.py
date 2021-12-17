import random
import requests
import datetime

import typesense

client = typesense.Client({
  'nodes': [{
    'host': 'localhost', # For Typesense Cloud use xxx.a1.typesense.net
    'port': '8108',      # For Typesense Cloud use 443
    'protocol': 'http'   # For Typesense Cloud use https
  }],
  'api_key': 'TEST',
  'connection_timeout_seconds': 10
})
coll = client.collections['pages']

words = list(map(lambda s: s.strip(), open("words.txt").readlines()))
long_words = list(filter(lambda s: len(s) > 4, words))

seconds = 0.0
for i in range(100):
  begin = datetime.datetime.now()
  q = " ".join(random.sample(words, 1))
  coll.documents.search({"q": q, "query_by": "title, abstract", "query_by_weights": "5, 1", "prefix": False})
  td = datetime.datetime.now() - begin
  seconds += td.seconds + 0.000001 * td.microseconds

print("Single Word: %s queries per second, %s ms" % (float(i) / seconds, seconds * 1000 / i))

seconds = 0.0
for i in range(100):
  begin = datetime.datetime.now()
  q = " ".join(random.sample(words, 3))
  coll.documents.search({"q": q, "query_by": "title, abstract", "query_by_weights": "5, 1", "prefix": False})
  td = datetime.datetime.now() - begin
  seconds += td.seconds + 0.000001 * td.microseconds

print("3 Word: %s queries per second, %s ms" % (float(i) / seconds, seconds * 1000 / i))

seconds = 0.0
for i in range(100):
  begin = datetime.datetime.now()
  q = random.choice(long_words)[:3]
  coll.documents.search({"q": q, "query_by": "title, abstract", "query_by_weights": "5, 1", "prefix": True})
  td = datetime.datetime.now() - begin
  seconds += td.seconds + 0.000001 * td.microseconds

print("Prefix: %s queries per second, %s ms" % (float(i) / seconds, seconds * 1000 / i))

