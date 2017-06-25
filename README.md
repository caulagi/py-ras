# rent-a-slogan

[![Build Status](https://travis-ci.org/caulagi/py-ras.svg?branch=master)](https://travis-ci.org/caulagi/py-ras)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/a5198bc52ab54e47be293a25fec1f037)](https://www.codacy.com/app/caulagi/py-ras?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=caulagi/py-ras&amp;utm_campaign=Badge_Grade)

A Python solution using uvloop and asyncpg. See [README][1] for problem
description. The recommended python version is **3.6.x**.

## Running locally

```bash
$ docker volume create rent_slogan
$ docker run \
    -v rent-slogan:/var/lib/postgresql/data \
    -e POSTGRES_PASSWORD=1234 \
    -e POSTGRES_DB=rent_slogan \
    -p 5432:5432 \
    -d postgres:9.6-alpine

$ python3 -m venv ~/.venv/ras
$ source ~/.venv/ras/bin/activate

$ python -m server
```

## Tests

```bash
py.test
```


[1]: https://github.com/caulagi/rent-a-slogan/blob/master/README.md
