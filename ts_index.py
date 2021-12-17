from generate import StreamDataGenerator
from itertools import islice
import datetime
import json

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

pages_schema = {
  'name': 'pages',
  'fields': [
    {'name': 'title', 'type': 'string' },
    {'name': 'url', 'type': 'string' },
    {'name': 'abstract', 'type': 'string' },
  ]
}
try:
  client.collections['pages'].delete()
except typesense.exceptions.ObjectNotFound:
  pass

client.collections.create(pages_schema)

g = StreamDataGenerator()
docs = g.parse()

i = 1

coll = client.collections['pages']
seconds = 0.0
try:
  batch_data = ""
  for d in docs:
    i += 1
    batch_data += json.dumps(d) + "\n"

    if i % 1000 == 0:
      begin = datetime.datetime.now()
      coll.documents.import_(batch_data.encode('ascii', errors="ignore"), {'action': 'create'})
      td = (datetime.datetime.now() - begin)
      seconds += td.seconds + td.microseconds * 0.000001
      batch_data = ""

    if i % 100000 == 0:
      print("Batch %s" % i)
finally:
  print("Indexed %s docs in %s seconds" % (i, seconds))
  print("%s docs per second" % (float(i) / seconds))