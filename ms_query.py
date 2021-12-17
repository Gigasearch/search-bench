import random
import requests
import datetime

SEARCH_URL = "http://127.0.0.1:7700/indexes/wiki/search"

words = list(map(lambda s: s.strip(), open("words.txt").readlines()))
long_words = list(filter(lambda s: len(s) > 4, words))

seconds = 0.0
for i in range(100):
  begin = datetime.datetime.now()
  q = " ".join(random.sample(words, 1))
  requests.post(SEARCH_URL, json={"q": q})
  td = datetime.datetime.now() - begin
  seconds += td.seconds + 0.000001 * td.microseconds

print("Single Word: %s queries per second, %s ms" % (float(i) / seconds, seconds * 1000 / i))

seconds = 0.0
for i in range(100):
  begin = datetime.datetime.now()
  q = " ".join(random.sample(words, 3))
  requests.post(SEARCH_URL, json={"q": q})
  td = datetime.datetime.now() - begin
  seconds += td.seconds + 0.000001 * td.microseconds

print("3 Word: %s queries per second, %s ms" % (float(i) / seconds, seconds * 1000 / i))

seconds = 0.0
for i in range(100):
  begin = datetime.datetime.now()
  q = random.choice(long_words)[:3]
  requests.post(SEARCH_URL, json={"q": q})
  td = datetime.datetime.now() - begin
  seconds += td.seconds + 0.000001 * td.microseconds

print("Prefix: %s queries per second, %s ms" % (float(i) / seconds, seconds * 1000 / i))

