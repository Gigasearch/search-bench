from generate import StreamDataGenerator
from itertools import islice
import datetime
import json

import requests

g = StreamDataGenerator()
docs = g.parse()

requests.delete("http://127.0.0.1:7700/indexes/wiki/documents")

i = 1

seconds = 0.0
try:
  batch_data = []
  for d in docs:
    i += 1
    d["id"] = i
    batch_data.append(d)

    if i % 10000 == 0:
      begin = datetime.datetime.now()
      requests.post("http://127.0.0.1:7700/indexes/wiki/documents", json=batch_data)
      td = (datetime.datetime.now() - begin)
      seconds += td.seconds + td.microseconds * 0.000001
      batch_data = []

    if i % 100000 == 0:
      print("Batch %s" % i)
finally:
  print("Indexed %s docs in %s seconds" % (i, seconds))
  print("%s docs per second" % (float(i) / seconds))