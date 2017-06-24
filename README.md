# rent-a-slogan

A Python solution using uvloop and asyncpg. See [README][1] for problem
description. The recommended python version is **3.6.x**.

## Running locally

```bash
$ docker volume create rent-slogan
$ docker run \
    -v rent-slogan:/var/lib/postgresql/data \
    -e POSTGRES_PASSWORD=1234 \
    -e POSTGRES_DB=rent-slogan \
    -p 5432:5432 \
    -d postgres:9.6-alpine

$ python3 -m venv ~/.venv/ras
$ source ~/.venv/ras/bin/activate

$ python -m server
```

## Tests

TODO

[1]: https://github.com/caulagi/rent-a-slogan/blob/master/README.md
