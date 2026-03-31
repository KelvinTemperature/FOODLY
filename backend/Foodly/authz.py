from functools import wraps

from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import abort

from db import db
from models import UserModel


def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()
        if not identity:
            abort(401, message='Authentication required')

        user = db.session.get(UserModel, int(identity))
        if not user or user.role != 'admin':
            abort(403, message='Admin privileges required')

        return fn(*args, **kwargs)

    return wrapper
