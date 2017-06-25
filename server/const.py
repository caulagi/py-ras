import os

PG_USERNAME = os.environ.get('PG_USERNAME', 'postgres')
PG_DATABASE = os.environ.get('PG_DATABASE', 'rent_slogan')
PG_PASSWORD = os.environ.get('PG_PASSWORD', '1234')


def connection_url():
    return 'postgresql://{}:{}@localhost/{}'.format(PG_USERNAME, PG_PASSWORD,
                                                    PG_DATABASE)
