from generate import StreamDataGenerator
from itertools import islice
import datetime
import json

g = StreamDataGenerator()
docs = g.parse()

i = 1
begin = datetime.datetime.now()
f = open("docs.jsonl", "w")
try:
  for d in docs:
    i += 1
    f.write(json.dumps(d) + "\n")

    if i % 100000 == 0:
      print("Batch %s" % i)
finally:
  seconds = (datetime.datetime.now() - begin).seconds
  print("Indexed %s docs in %s seconds" % (i, seconds))
  print("%s docs per second" % (float(i) / seconds))