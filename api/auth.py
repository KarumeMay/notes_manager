from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.user import User
from extensions import db
from schemas.user_schema import UserSchema

bp = Blueprint('auth', __name__, url_prefix='/auth')
schema = UserSchema()


@bp.route('/register', methods=['POST'])
def register():
    data = schema.load(request.json)
    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return schema.dump(user), 201


@bp.route('/login', methods=['POST'])
def login():
    data = schema.load(request.json)
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        token = create_access_token(identity=user.id)
        return jsonify(access_token=token)
    return jsonify({'msg': 'Bad credentials'}), 401
