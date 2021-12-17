# Search benchmarks

This is the source code for [Gigasearch benchmarking blog post](https://blog.gigasearch.co/elasticsearch-against-competitors/). 

Requires Python 3 and Docker.

## Run: download data

Download and extract abstracts dump from [Wikipedia archive](https://dumps.wikimedia.org/enwiki/) renaming it to `enwiki-20210720-abstract.xml` (or change the date in `*_index.py`),

## Run: Elasticsearch

```
pip install elasticsearch
docker-compose up -d -f ./es-docker-compose.yaml
python3 ./es_index.py
python3 ./es_query.py
```

## Run: Meilisearch

```
docker-compose up -d -f ./ms-docker-compose.yaml
python3 ./ms_index.py
python3 ./ms_query.py
```

## Run: PostgreSQL

```
pip install psycopg2
docker-compose up -d -f ./pg-docker-compose.yaml
python3 ./pg_index.py
python3 ./pg_query.py
```

## Run: RediSearch

```
pip install redisearch
docker-compose up -d -f ./redis-docker-compose.yaml
python3 ./redis_index.py
python3 ./redis_query.py
```

## Run: TypeSense

```
pip install typesense
docker-compose up -d -f ./ts-docker-compose.yaml
python3 ./ts_index.py
python3 ./ts_query.py
```

