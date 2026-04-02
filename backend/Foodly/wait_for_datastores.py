import os
import time

from pymongo import MongoClient
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


def _build_mysql_uri():
    explicit_uri = os.environ.get('DATABASE_URL')
    if explicit_uri:
        return explicit_uri

    mysql_user = os.environ.get('MYSQL_USER', 'root')
    mysql_password = os.environ.get('MYSQL_PASSWORD', '')
    mysql_host = os.environ.get('MYSQL_HOST', '127.0.0.1')
    mysql_port = int(os.environ.get('MYSQL_PORT', '3306'))
    mysql_database = os.environ.get('MYSQL_DATABASE', 'foodly_auth')

    return str(
        URL.create(
            drivername='mysql+pymysql',
            username=mysql_user,
            password=mysql_password,
            host=mysql_host,
            port=mysql_port,
            database=mysql_database,
        )
    )


def _wait_for_mysql(timeout_seconds, interval_seconds):
    mysql_uri = _build_mysql_uri()
    deadline = time.time() + timeout_seconds
    last_error = None

    while time.time() < deadline:
        try:
            engine = create_engine(mysql_uri, pool_pre_ping=True)
            with engine.connect() as connection:
                connection.execute(text('SELECT 1'))
            engine.dispose()
            print('MySQL is reachable.')
            return
        except Exception as exc:  # pragma: no cover
            last_error = exc
            print(f'Waiting for MySQL... ({exc})')
            time.sleep(interval_seconds)

    raise RuntimeError(f'MySQL is not reachable: {last_error}')


def _wait_for_mongo(timeout_seconds, interval_seconds):
    mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017')
    if mongo_uri.startswith('mongomock://'):
        print('MongoDB check skipped for mongomock URI.')
        return

    deadline = time.time() + timeout_seconds
    last_error = None

    while time.time() < deadline:
        try:
            client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            client.admin.command('ping')
            client.close()
            print('MongoDB is reachable.')
            return
        except Exception as exc:  # pragma: no cover
            last_error = exc
            print(f'Waiting for MongoDB... ({exc})')
            time.sleep(interval_seconds)

    raise RuntimeError(f'MongoDB is not reachable: {last_error}')


def main():
    timeout_seconds = int(os.environ.get('DB_WAIT_TIMEOUT_SECONDS', '90'))
    interval_seconds = int(os.environ.get('DB_WAIT_INTERVAL_SECONDS', '3'))

    _wait_for_mysql(timeout_seconds, interval_seconds)
    _wait_for_mongo(timeout_seconds, interval_seconds)
    print('All datastores are reachable.')


if __name__ == '__main__':
    main()
