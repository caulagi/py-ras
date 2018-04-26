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
```

#### Dependencies

```bash
# for just running the project
$ pip install -r requirements.txt

# for running tests and code quality checks
$ pip install -r test/requirements.txt
```

#### Finally...

```bash
$ python -m server
```

```bash
$ nc localhost 25001
status
Total number of slogans: 10
Number of rents: 2
Number of connected clients: 3

add::Just do it
Just do it
add::Just do it
error: slogan already exists

rent
OK: id:4 title:t1
Slogan id 4 has expired
```

## Tests

```bash
py.test
```


[1]: https://github.com/caulagi/rent-a-slogan/blob/master/README.md
