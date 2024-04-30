from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from wtforms_sqlalchemy.fields import QuerySelectField
from warehouse.models import Location, Inventory

class AddProductForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    price = IntegerField('Цена', validators=[DataRequired(), NumberRange(min=0)])

class AddLocationForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])

class AddToInventoryForm(FlaskForm):
    location_id = QuerySelectField(
        get_label='name',
        validators=[DataRequired()],
        query_factory=lambda product_id: Location.query.filter(                 # Фильтрация всех складов, к которым еще не привязан данный товар
            ~Location.inventories.any(Inventory.product_id == product_id)),)

    def __init__(self, product_id, *args, **kwargs):
        super(AddToInventoryForm, self).__init__(*args, **kwargs)
        self.product_id = product_id
        self.location_id.query = self.location_id.query_factory(
            self.product_id)

class DeleteFromInventoryForm(FlaskForm):
    location_id = QuerySelectField(
        get_label='name',
        validators=[DataRequired()],
        query_factory=lambda product_id: Location.query.filter(                 # Фильтрация всех складов, к которым уже привязан данный товар
            Location.inventories.any(Inventory.product_id == product_id)))

    def __init__(self, product_id, *args, **kwargs):
        super(DeleteFromInventoryForm, self).__init__(*args, **kwargs)
        self.product_id = product_id
        self.location_id.query = self.location_id.query_factory(
            self.product_id)

class ChangeQuantityForm(FlaskForm):
    quantity = IntegerField('Количество товара',
                            validators=[NumberRange(min=0)])
    location_id = QuerySelectField(
        get_label='name',
        validators=[DataRequired()],
        query_factory=lambda product_id: Location.query.filter(                 # Фильтрация всех складов, к которым уже привязан данный товар
            Location.inventories.any(Inventory.product_id == product_id)))

    def __init__(self, product_id, *args, **kwargs):
        super(ChangeQuantityForm, self).__init__(*args, **kwargs)
        self.product_id = product_id
        self.location_id.query = self.location_id.query_factory(
            self.product_id)

class FilterByLocation(FlaskForm):
    location = QuerySelectField(
        get_label='name', query_factory=lambda: Location.query)
