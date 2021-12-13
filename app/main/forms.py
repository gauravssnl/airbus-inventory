from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError


from ..models import User, Product, ProductCategory


class ProductForm(FlaskForm):
    name = StringField('Product name', validators=[
                       DataRequired(), Length(0, 64)])
    description = StringField('Product Description', validators=[
                              DataRequired(), Length(0, 64)])
    quantity = IntegerField('Quantity')
    category = SelectField('Product Category', choices=[(
        'Commercial', 'Commercial'), ('Space', 'Space'), ('Helicopter', 'Helicopter')])
    submit = SubmitField('Submit')
