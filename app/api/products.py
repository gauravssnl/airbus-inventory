from flask import jsonify, request, current_app, url_for

from app.api import utils
from app.exceptions import ValidationError
from . import api
from ..models import ProductCategory, Product
from .. import db


@api.route('/products')
def get_products():
    products = utils.get_all_table_data(Product)
    return jsonify([product.to_json() for product in products])


@api.route('/products/<int:id>')
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(product.to_json())


@api.route('/products', methods=['POST'])
def add_product():
    product = Product.from_json(request.json)
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_json()), 201


@api.route('/products', methods=['PUT'])
def update_product():
    id = request.json.get('id')
    product = utils.get_table_data_by_id(Product, id)
    updated_product = Product.from_json(request.json)
    product.update_data(updated_product)
    db.session.add(product)
    db.session.commit()
    response = jsonify(product.to_json())
    response.status_code = 200
    return response


@api.route('/products/<int:id>', methods=["DELETE"])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    response = jsonify({'error': None, 'message': "Deleted successfully"})
    response.status_code = 200
    return response
