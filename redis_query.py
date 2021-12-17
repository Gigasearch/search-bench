import random
import redisearch
import datetime

client = redisearch.Client("test-giga")

words = list(map(lambda s: s.strip(), open("words.txt").readlines()))
long_words = list(filter(lambda s: len(s) > 4, words))

seconds = 0.0
for i in range(100):
  begin = datetime.datetime.now()
  res = client.search(" ".join(random.sample(words, 1)))
  td = datetime.datetime.now() - begin
  seconds += td.seconds + 0.000001 * td.microseconds

print("Single Word: %s queries per second, %s ms" % (float(i) / seconds, seconds * 1000 / i))

seconds = 0.0
for i in range(1000):
  begin = datetime.datetime.now()
  res = client.search(" ".join(random.sample(words, 3)))
  td = datetime.datetime.now() - begin
  seconds += td.seconds + 0.000001 * td.microseconds

print("3 Word: %s queries per second, %s ms" % (float(i) / seconds, seconds * 1000 / i))

seconds = 0.0
for i in range(100):
  begin = datetime.datetime.now()
  res = client.search("|".join(random.sample(words, 3)))
  td = datetime.datetime.now() - begin
  seconds += td.seconds + 0.000001 * td.microseconds

print("3 Word OR: %s queries per second, %s ms" % (float(i) / seconds, seconds * 1000 / i))

seconds = 0.0
for i in range(100):
  begin = datetime.datetime.now()
  q = '"' + (" ".join(random.sample(long_words, 2))) + '"'
  res = client.search(q)
  td = datetime.datetime.now() - begin
  seconds += td.seconds + 0.000001 * td.microseconds

print("Exact Phrase: %s queries per second, %s ms" % (float(i) / seconds, seconds * 1000 / i))

seconds = 0.0
for i in range(100):
  begin = datetime.datetime.now()
  res = client.search(random.choice(long_words)[:3] + "*")
  td = datetime.datetime.now() - begin
  seconds += td.seconds + 0.000001 * td.microseconds

print("Prefix: %s queries per second, %s ms" % (float(i) / seconds, seconds * 1000 / i))

