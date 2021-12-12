from flask import jsonify, request, current_app, url_for

from . import api
from . import utils
from ..models import User
from .. import db


@api.route('/users')
def get_users():
    users = User.query.all()
    return jsonify([user.to_json() for user in users])


@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())


@api.route('/users', methods=['POST'])
def add_user():
    user = User.from_json(request.json)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_json()), 201


@api.route('/users', methods=['PUT'])
def update_user():
    id = request.json.get('id')
    user = utils.get_table_data_by_id(User, id)
    updated_user = User.from_json(request.json)
    user.update_data(updated_user)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_json())
    response.status_code = 200
    return response


@api.route('/users/<int:id>', methods=["DELETE"])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    response = jsonify({'error': None, 'message': "Deleted successfully"})
    response.status_code = 200
    return response
