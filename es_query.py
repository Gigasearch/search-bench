import random
import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch(['localhost:9200'])

INDEX_NAME = 'giga-bench-wiki'

words = list(map(lambda s: s.strip(), open("words.txt").readlines()))
long_words = list(filter(lambda s: len(s) > 4, words))

seconds = 0.0
for i in range(100):
  begin = datetime.datetime.now()
  q = " ".join(random.sample(words, 1))
  es.search({
    "query": {
      "multi_match" : {
        "query":    q,
        "fields": [ "title", "abstract" ],
        "operator":   "and"
      }
    }
  }, index=INDEX_NAME)
  td = datetime.datetime.now() - begin
  seconds += td.seconds + 0.000001 * td.microseconds

print("Single Word: %s queries per second, %s ms" % (float(i) / seconds, seconds * 1000 / i))

seconds = 0.0
for i in range(100):
  begin = datetime.datetime.now()
  q = " ".join(random.sample(words, 3))
  es.search({
    "query": {
      "multi_match" : {
        "query":    q,
        "fields": [ "title", "abstract" ],
        "operator":   "and"
      }
    }
  }, index=INDEX_NAME)
  td = datetime.datetime.now() - begin
  seconds += td.seconds + 0.000001 * td.microseconds

print("3 Word: %s queries per second, %s ms" % (float(i) / seconds, seconds * 1000 / i))

seconds = 0.0
for i in range(100):
  begin = datetime.datetime.now()
  q = " OR ".join(random.sample(words, 3))
  es.search({
    "query": {
      "multi_match" : {
        "query":    q,
        "fields": [ "title", "abstract" ],
        "operator":   "or"
      }
    }
  }, index=INDEX_NAME)
  td = datetime.datetime.now() - begin
  seconds += td.seconds + 0.000001 * td.microseconds

print("3 Word OR: %s queries per second, %s ms" % (float(i) / seconds, seconds * 1000 / i))

seconds = 0.0
for i in range(100):
  begin = datetime.datetime.now()
  q = '"' + (" ".join(random.sample(long_words, 2))) + '"'
  es.search({
    "query": {
      "match_phrase" : {
        "abstract":    q
      }
    }
  }, index=INDEX_NAME)
  td = datetime.datetime.now() - begin
  seconds += td.seconds + 0.000001 * td.microseconds

print("Exact Phrase: %s queries per second, %s ms" % (float(i) / seconds, seconds * 1000 / i))

seconds = 0.0
for i in range(100):
  begin = datetime.datetime.now()
  q = random.choice(long_words)[:3]
  es.search({
    "query": {
      "prefix" : {
        "abstract":    q
      }
    }
  }, index=INDEX_NAME)
  td = datetime.datetime.now() - begin
  seconds += td.seconds + 0.000001 * td.microseconds

print("Prefix: %s queries per second, %s ms" % (float(i) / seconds, seconds * 1000 / i))

