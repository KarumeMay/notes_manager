from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from extensions import db
from models.category import Category
from schemas.category_schema import CategorySchema

bp = Blueprint('categories', __name__, url_prefix='/categories')
schema = CategorySchema()
many_schema = CategorySchema(many=True)


@bp.route('/', methods=['GET'])
@jwt_required()
def list_categories():
    cats = Category.query.all()
    return many_schema.dump(cats)


@bp.route('/', methods=['POST'])
@jwt_required()
def create_category():
    data = schema.load(request.json)
    cat = Category(**data)
    db.session.add(cat)
    db.session.commit()
    return schema.dump(cat), 201
