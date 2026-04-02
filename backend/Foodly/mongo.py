import os

from pymongo import MongoClient

try:
    import mongomock
except ImportError:  # pragma: no cover
    mongomock = None


_mongo_client = None
_mongo_db = None


def init_mongo(app):
    global _mongo_client, _mongo_db

    mongo_uri = app.config['MONGO_URI']
    mongo_db_name = app.config['MONGO_DB_NAME']

    if mongo_uri.startswith('mongomock://'):
        if mongomock is None:
            raise RuntimeError('mongomock is required for mongomock:// URIs')
        _mongo_client = mongomock.MongoClient()
    else:
        _mongo_client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        _mongo_client.admin.command('ping')

    _mongo_db = _mongo_client[mongo_db_name]
    _mongo_db['orders'].create_index('id', unique=True)
    _mongo_db['counters'].update_one(
        {'_id': 'orders'},
        {'$setOnInsert': {'seq': 0}},
        upsert=True,
    )


def get_mongo_db():
    if _mongo_db is None:
        raise RuntimeError('MongoDB client is not initialized')
    return _mongo_db


def build_mongo_uri_from_env():
    return os.environ.get('MONGO_URI', 'mongodb://localhost:27017')
