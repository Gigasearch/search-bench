from generate import StreamDataGenerator
from itertools import islice
import redisearch
import datetime

SCHEMA = (
    redisearch.TextField("title", weight=5.0),
    redisearch.TextField("abstract"),
    redisearch.TextField("url")
)

client = redisearch.Client("test-giga")

definition = redisearch.IndexDefinition(prefix=['docs:'])

client.redis.flushdb()
client.create_index(SCHEMA, definition=definition)

g = StreamDataGenerator()
docs = g.parse()

i = 1
batcher = client.batch_indexer(10000)
try:
  for d in docs:
    i += 1
    begin = datetime.datetime.now()
    batcher.add_document(doc_id="docs:%s" % i, **d)
    seconds = (datetime.datetime.now() - begin).seconds

    if i % 100000 == 0:
      print("Batch %s" % i)
finally:
  print("Indexed %s docs in %s seconds" % (i, seconds))
  print("%s docs per second" % (float(i) / seconds))