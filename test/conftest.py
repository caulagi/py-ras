import os


def pytest_configure():
    os.environ['PG_DATABASE'] = os.environ.get('PG_DATABASE', 'slogan_test')
    os.environ['PG_PASSWORD'] = os.environ.get('PG_PASSWORD', '')
