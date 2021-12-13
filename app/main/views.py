from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response
import sqlalchemy
from flask_login import login_required, current_user
from . import main
from .forms import ProductForm
from .. import db
from ..models import User, Product, ProductCategory


@main.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        products = Product.query.all()
        return render_template('products.html', products=products)
    else:
        flash('You need to login first.')
        return redirect(url_for('auth.login'))

@main.route('/edit-product/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    form = ProductForm(product=product)
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.quantity = form.quantity.data
        category = ProductCategory.query.filter_by(
            name=form.category.data).first()
        if category is None:
            category = ProductCategory()
            category.name = form.category.data
            db.session.add(category)
        product.category = category
        db.session.add(product)
        try:
            db.session.commit()
            flash('The Product details have been saved.')
        except sqlalchemy.exc.IntegrityError:
            flash('Product with given product name already exists')
            return
        return redirect(url_for('.index'))
    form.name.data = product.name
    form.description.data = product.description
    form.category.data = product.category
    form.name.data = product.name
    form.quantity.data = product.quantity
    return render_template('edit_product.html', form=form, product=product, mode="Edit")


@main.route('/add-product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product()
        product.name = form.name.data
        product.description = form.description.data
        product.quantity = form.quantity.data
        category = ProductCategory.query.filter_by(
            name=form.category.data).first()
        if category is None:
            category = ProductCategory()
            category.name = form.category.data
            db.session.add(category)
        product.category = category
        db.session.add(product)
        try:
            db.session.commit()
            flash('The Product details have been saved.')
            return redirect(url_for('.index'))
        except sqlalchemy.exc.IntegrityError:
            flash('Product with given product name already exists')
    return render_template('edit_product.html', form=form, mode="Add")

@main.route('/delete-product/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    try:
        db.session.delete(product)
        db.session.commit()
        flash('The Product has been deleted.')
    except Exception:
            flash('Product deletion failed')
            return
    return redirect(url_for('.index'))
