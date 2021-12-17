import random
import datetime

import psycopg2

connection = psycopg2.connect(user="postgres", password="pass", host="127.0.0.1", port="15432", database="pages")
cursor = connection.cursor()

words = list(map(lambda s: s.strip(), open("words.txt").readlines()))
long_words = list(filter(lambda s: len(s) > 4, words))

seconds = 0.0
for i in range(100):
  begin = datetime.datetime.now()
  q = " ".join(random.sample(words, 1))
  cursor.execute("SELECT * FROM pages WHERE (setweight(to_tsvector('english'::regconfig, title), 'A') || setweight(to_tsvector('english'::regconfig, abstract), 'B')) @@ websearch_to_tsquery('english'::regconfig, %s) LIMIT 10000;", (q, )) 
  td = datetime.datetime.now() - begin
  seconds += td.seconds + 0.000001 * td.microseconds

print("Single Word: %s queries per second, %s ms" % (float(i) / seconds, seconds * 1000 / i))

seconds = 0.0
for i in range(100):
  begin = datetime.datetime.now()
  q = " & ".join(random.sample(words, 3))
  cursor.execute("SELECT * FROM pages WHERE (setweight(to_tsvector('english'::regconfig, title), 'A') || setweight(to_tsvector('english'::regconfig, abstract), 'B')) @@ websearch_to_tsquery('english'::regconfig, %s) LIMIT 10000;", (q, )) 
  td = datetime.datetime.now() - begin
  seconds += td.seconds + 0.000001 * td.microseconds

print("3 Word: %s queries per second, %s ms" % (float(i) / seconds, seconds * 1000 / i))

seconds = 0.0
for i in range(100):
  begin = datetime.datetime.now()
  q = " ".join(random.sample(words, 3))
  cursor.execute("SELECT * FROM pages WHERE (setweight(to_tsvector('english'::regconfig, title), 'A') || setweight(to_tsvector('english'::regconfig, abstract), 'B')) @@ websearch_to_tsquery('english'::regconfig, %s) LIMIT 10000;", (q, )) 
  td = datetime.datetime.now() - begin
  seconds += td.seconds + 0.000001 * td.microseconds

print("3 Word OR: %s queries per second, %s ms" % (float(i) / seconds, seconds * 1000 / i))

seconds = 0.0
for i in range(100):
  begin = datetime.datetime.now()
  q = '"' + " ".join(random.sample(long_words, 2)) + '"';
  cursor.execute("SELECT * FROM pages WHERE (setweight(to_tsvector('english'::regconfig, title), 'A') || setweight(to_tsvector('english'::regconfig, abstract), 'B')) @@ websearch_to_tsquery('english'::regconfig, %s) LIMIT 10000;", (q, )) 
  td = datetime.datetime.now() - begin
  seconds += td.seconds + 0.000001 * td.microseconds

print("Exact Phrase: %s queries per second, %s ms" % (float(i) / seconds, seconds * 1000 / i))

seconds = 0.0
for i in range(100):
  begin = datetime.datetime.now()
  q = random.choice(long_words)[:3] + ":*"
  cursor.execute("SELECT * FROM pages WHERE (setweight(to_tsvector('english'::regconfig, title), 'A') || setweight(to_tsvector('english'::regconfig, abstract), 'B')) @@ websearch_to_tsquery('english'::regconfig, %s) LIMIT 10000;", (q, )) 
  td = datetime.datetime.now() - begin
  seconds += td.seconds + 0.000001 * td.microseconds

print("Prefix: %s queries per second, %s ms" % (float(i) / seconds, seconds * 1000 / i))

