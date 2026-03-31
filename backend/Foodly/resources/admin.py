from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from authz import admin_required
from db import db
from models import UserModel
from schemas import AdminRoleUpdateSchema

blueprint = Blueprint('admin', __name__, description='Admin API')


@blueprint.route('/admin/users')
class AdminUsers(MethodView):
    @blueprint.response(200)
    @admin_required
    def get(self):
        users = UserModel.query.order_by(UserModel.id.asc()).all()
        return {
            'users': [
                {
                    'id': user.id,
                    'full_name': user.full_name,
                    'email': user.email,
                    'phone': user.phone,
                    'role': user.role,
                }
                for user in users
            ]
        }


@blueprint.route('/admin/users/<int:user_id>/role')
class AdminUserRole(MethodView):
    @blueprint.arguments(AdminRoleUpdateSchema)
    @blueprint.response(200)
    @admin_required
    def put(self, payload, user_id):
        try:
            user = db.session.get(UserModel, user_id)
            if not user:
                abort(404, message='User not found')

            user.role = payload['role']
            db.session.commit()
            return {
                'id': user.id,
                'email': user.email,
                'role': user.role,
            }
        except SQLAlchemyError as exc:
            abort(500, message=str(exc))
