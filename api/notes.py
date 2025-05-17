from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.note import Note
from schemas.note_schema import NoteSchema

bp = Blueprint('notes', __name__, url_prefix='/notes')
schema = NoteSchema()
many_schema = NoteSchema(many=True)


@bp.route('/', methods=['GET'])
@jwt_required()
def list_notes():
    user_id = get_jwt_identity()
    search = request.args.get('search')
    tag = request.args.get('tag')
    from services.note_service import get_notes_for_user
    notes = get_notes_for_user(user_id, search, tag)
    return many_schema.dump(notes)


@bp.route('/', methods=['POST'])
@jwt_required()
def create_note():
    data = schema.load(request.json)
    data['user_id'] = get_jwt_identity()
    note = Note(**data)
    db.session.add(note)
    db.session.commit()
    return schema.dump(note), 201


@bp.route('/<int:note_id>/', methods=['PUT'])
@jwt_required()
def update_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != get_jwt_identity():
        return jsonify({'msg': 'Forbidden'}), 403
    data = schema.load(request.json, partial=True)
    for k, v in data.items():
        setattr(note, k, v)
    db.session.commit()
    return schema.dump(note)


@bp.route('/<int:note_id>/', methods=['DELETE'])
@jwt_required()
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != get_jwt_identity():
        return jsonify({'msg': 'Forbidden'}), 403
    db.session.delete(note)
    db.session.commit()
    return '', 204
