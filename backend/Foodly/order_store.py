from datetime import datetime, timezone

from pymongo import ReturnDocument

from mongo import get_mongo_db


def _utcnow():
    return datetime.now(timezone.utc)


def _orders_collection():
    return get_mongo_db()['orders']


def _counters_collection():
    return get_mongo_db()['counters']


def _next_order_id():
    counter = _counters_collection().find_one_and_update(
        {'_id': 'orders'},
        {'$inc': {'seq': 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return int(counter['seq'])


def _serialize_order(document):
    if not document:
        return None

    payload = dict(document)
    payload.pop('_id', None)
    return payload


def create_order(order_data):
    payload = dict(order_data)
    now = _utcnow()
    payload['id'] = _next_order_id()
    payload['created_at'] = now
    payload['updated_at'] = now

    _orders_collection().insert_one(payload)
    return _serialize_order(payload)


def get_order(order_id):
    document = _orders_collection().find_one({'id': int(order_id)})
    return _serialize_order(document)


def list_orders():
    cursor = _orders_collection().find().sort('id', 1)
    return [_serialize_order(document) for document in cursor]


def replace_order(order_id, order_data):
    payload = dict(order_data)
    payload['id'] = int(order_id)
    payload['updated_at'] = _utcnow()

    result = _orders_collection().replace_one({'id': int(order_id)}, payload)
    if result.matched_count == 0:
        return None

    return get_order(order_id)


def delete_order(order_id):
    result = _orders_collection().delete_one({'id': int(order_id)})
    return result.deleted_count > 0
