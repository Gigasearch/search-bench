from generate import StreamDataGenerator
from itertools import islice
import json
import datetime

from elasticsearch import Elasticsearch
es = Elasticsearch(['localhost:9200'])

INDEX_NAME = 'giga-bench-wiki'

es.indices.delete(index=INDEX_NAME, ignore=[400, 404])
es.indices.create(index=INDEX_NAME, ignore=400)

g = StreamDataGenerator()
docs = g.parse()

i = 1
seconds = 0.0
batch_data = ""
try:
  for d in docs:
    if i % 10000 == 0:
      print("Batch: %s" % i)
      begin = datetime.datetime.now()
      es.bulk(batch_data)
      td = (datetime.datetime.now() - begin)
      seconds += td.seconds + td.microseconds * 0.000001
      batch_data = ""

    batch_data += """{ "index" : { "_index" : "%s", "_id" : %s } })\n""" % (INDEX_NAME, i)
    batch_data += """{ "abstract": "%s", "title": "%s", "url": "%s" }\n""" % (d["abstract"], d["title"], d["url"])
    i += 1
finally:
  print("Batch: %s" % i)
  begin = datetime.datetime.now()
  es.bulk(batch_data)

  td = (datetime.datetime.now() - begin)
  seconds += td.seconds + td.microseconds * 0.000001

  print("Indexed %s docs in %s seconds" % (i, seconds))
  print("%s docs per second" % (float(i) / seconds))