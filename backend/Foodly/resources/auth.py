from flask.views import MethodView
from flask_jwt_extended import create_access_token
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import UserModel
from schemas import AuthLoginSchema, AuthResponseSchema, UserRegisterSchema

blueprint = Blueprint('auth', __name__, description='Authentication API')


@blueprint.route('/auth/register')
class Register(MethodView):
    @blueprint.arguments(UserRegisterSchema)
    @blueprint.response(201, AuthResponseSchema)
    def post(self, payload):
        try:
            existing_user = UserModel.query.filter_by(email=payload['email']).first()
            if existing_user:
                abort(409, message='User with this email already exists')

            user = UserModel(
                full_name=payload['full_name'],
                email=payload['email'],
                phone=payload.get('phone'),
                role=payload.get('role', 'customer'),
            )
            user.set_password(payload['password'])

            db.session.add(user)
            db.session.commit()

            token = create_access_token(identity=str(user.id))
            return {
                'access_token': token,
                'user': {
                    'id': user.id,
                    'full_name': user.full_name,
                    'email': user.email,
                    'phone': user.phone,
                    'role': user.role,
                },
            }
        except SQLAlchemyError as e:
            abort(500, message=str(e))


@blueprint.route('/auth/login')
class Login(MethodView):
    @blueprint.arguments(AuthLoginSchema)
    @blueprint.response(200, AuthResponseSchema)
    def post(self, payload):
        try:
            user = UserModel.query.filter_by(email=payload['email']).first()
            if not user or not user.check_password(payload['password']):
                abort(401, message='Invalid email or password')

            token = create_access_token(identity=str(user.id))
            return {
                'access_token': token,
                'user': {
                    'id': user.id,
                    'full_name': user.full_name,
                    'email': user.email,
                    'phone': user.phone,
                    'role': user.role,
                },
            }
        except SQLAlchemyError as e:
            abort(500, message=str(e))
