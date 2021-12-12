from flask import jsonify, request, current_app, url_for
from flask_jwt_extended import jwt_required

from . import api
from . import utils
from ..models import ProductCategory, Product
from .. import db


@api.route('/categories')
@jwt_required()
def get_product_categories():
    product_categories = ProductCategory.query.all()
    fetch_products_flag = False
    request_args = request.args
    if (request.args.get('fetchProducts') and request.args.get('fetchProducts') == "true"
            or request.args.get('fetchProducts') == "True"):
        fetch_products_flag = True
    return jsonify([category.to_json(fetch_products_flag=fetch_products_flag) for category in product_categories])


@api.route('/categories/<int:id>')
@jwt_required()
def get_product_category(id):
    product_category = ProductCategory.query.get_or_404(id)
    fetch_products_flag = False
    request_args = request.args
    if (request.args.get('fetchProducts') and request.args.get('fetchProducts') == "true"
            or request.args.get('fetchProducts') == "True"):
        fetch_products_flag = True
    return jsonify(product_category.to_json(fetch_products_flag=fetch_products_flag))


@api.route('/categories', methods=['POST'])
@jwt_required()
def add_product_category():
    product_category = ProductCategory.from_json(request.json)
    db.session.add(product_category)
    db.session.commit()
    response = jsonify(product_category.to_json())
    response.status_code = 201
    return response


@api.route('/categories', methods=['PUT'])
@jwt_required()
def update_product_category():
    id = request.json.get('id')
    product_category = utils.get_table_data_by_id(ProductCategory, id)
    updated_product_category = ProductCategory.from_json(request.json)
    product_category.update_data(updated_product_category)
    db.session.add(product_category)
    db.session.commit()
    response = jsonify(product_category.to_json())
    response.status_code = 200
    return response


@api.route('/categories/<int:id>', methods=["DELETE"])
@jwt_required()
def delete_product_category(id):
    product_category = ProductCategory.query.get_or_404(id)
    db.session.delete(product_category)
    db.session.commit()
    return jsonify({'error': None, 'message': "Deleted successfully"}), 200


@api.route('/categories/<int:id>/products/', methods=['POST'])
@jwt_required()
def add_product_for_category(id):
    product_category = ProductCategory.query.get_or_404(id)
    product = Product.from_json(request.json)
    db.session.add(product)
    db.session.commit()
    return jsonify(product_category.to_json()), 200
