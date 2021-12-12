from flask import request

from app.exceptions import ValidationError
from . import utils
from ..models import Product


def get_table_data_by_id(table, id):
    if id is None:
        raise ValidationError('Invalid Input Data')
    table_data = table.query.filter_by(id=id).first()
    if table_data is None:
        raise ValidationError('Data with given Id {} not found'.format(id))
    return table_data


def get_all_table_data(table):
    table_data = table.query.all()
    return table_data
