from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from . import db
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

class ProductCategory:
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True)
    products = db.relationship('Product', backref='category', lazy='dynamic')

    @staticmethod
    def insert_categories():
        pass
    def __repr__(self):
        return '<ProductCategory %r>' % self.name
class Product:
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    description = db.Column(db.String(256))
    quantity = db.Column(db.Integer)

    def __repr__(self):
        return '<Product %r>' % self.name