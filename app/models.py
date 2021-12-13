from os import name
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.exceptions import ValidationError
from . import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def from_json(json_user):
        data = {}
        data['email'] = json_user.get('email')
        data['username'] = json_user.get('username')
        data['password'] = json_user.get('password')
        if data['email'] is None or data['email'] == '':
            raise ValidationError("Invalid Input Data: Email can't be empty")
        if data['username'] is None or data['username'] == '':
            raise ValidationError(
                "Invalid Input Data: Username can't be empty")
        if data['password'] is None or data['password'] == '':
            raise ValidationError(
                "Invalid Input Data: Password can't be empty")
        user = User(**data)
        return user

    def to_json(self):
        json_user = {
            'id': self.id,
            'email': self.email,
            'username': self.username
        }
        return json_user

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


class ProductCategory(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True)
    products = db.relationship('Product', backref='category', lazy='dynamic')

    def __init__(self, **kwargs):
        super(ProductCategory, self).__init__(**kwargs)

    @staticmethod
    def insert_categories():
        pass

    def __repr__(self):
        return '<ProductCategory %r>' % self.name

    def to_json(self, fetch_products_flag=False):
        json_product_category = {
            'id': self.id,
            'name': self.name
        }
        if fetch_products_flag and self.products:
            json_product_category['products'] = [
                product.to_json() for product in self.products.all()]

        return json_product_category

    @staticmethod
    def from_json(json_product_category):
        data = {}
        data['name'] = json_product_category.get('name')
        if data['name'] is None or data['name'] == '':
            raise ValidationError('Invalid Input Data')
        # if json_product_category.get('products') is not None or json_product_category.get('products') != '':
        #     data['products'] = json_product_category.get('products')
        # else:
        #     data['products'] = []
        return ProductCategory(**data)

    def update_data(self, other):
        # if other is not Product:
        #     raise ValidationError("other must be a type of Product")
        properties = ['name']
        for property in properties:
            setattr(self, property, getattr(other, property))


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    description = db.Column(db.String(256))
    quantity = db.Column(db.Integer)

    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)

    def __repr__(self):
        return '<Product %r>' % self.name

    def to_json(self):
        json_product = {
            'id': self.id,
            'name': self.name,
            'category': self.category_id,
            'description': self.description,
            'quantity': self.quantity
        }
        return json_product

    @staticmethod
    def from_json(json_product):
        data = {}
        data['name'] = json_product.get('name')
        category = json_product.get('category')
        data['description'] = json_product.get('description')
        data['quantity'] = json_product.get('quantity')
        if (
            data['name'] is None or data['name'] == ''
            or category is None or category == ''
            or data['description'] is None or data['description'] == ''
            or data['quantity'] is None or data['quantity'] == ''
        ):
            raise ValidationError('Invalid Input Data')
        product_category = ProductCategory.query.filter_by(
            name=category).first()
        if product_category is None:
            raise ValidationError(
                'Invalid Input Data: Product Category not found')
        data['category_id'] = product_category.id
        return Product(**data)

    def update_data(self, other):
        # if other is not Product:
        #     raise ValidationError("other must be a type of Product")
        properties = ['name', 'description', 'quantity']
        for property in properties:
            setattr(self, property, getattr(other, property))
