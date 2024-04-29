from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc
from forms import AddLocationForm, AddProductForm
from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import DataRequired, NumberRange
from wtforms_sqlalchemy.fields import QuerySelectField
from database_auth import database_username, database_password, database_host, database_name
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{database_username}:{database_password}@{database_host}/{database_name}'
app.config['SECRET_KEY'] = '\xa0\xf1\xf5x\xf7\x137MP\x1f&\xea\x99]\xf5\x12\xbe<X\x07\xa8gY\xe7\xd8\xa7U\xd0\t\xfd_$'

db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'product.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey(
        'location.id'), nullable=False)
    quantity = db.Column(db.Integer, db.CheckConstraint(
        'quantity >= 0'), default=0)
    product = db.relationship(
        'Product', backref=db.backref('inventories', lazy='dynamic'))
    location = db.relationship(
        'Location', backref=db.backref('inventories', lazy='dynamic'))


with app.app_context():
    db.create_all()


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


def get_context():
    return {
        'products': Product.query.all(),
        'locations': Location.query.all(),
        'add_product_form': AddProductForm(),
        'add_location_form': AddLocationForm(),
        'add_to_inventory_form': AddToInventoryForm,
        'delete_from_inventory_form': DeleteFromInventoryForm,
        'change_quantity_form': ChangeQuantityForm,
        'filter_by_location': FilterByLocation(),
    }


@app.route('/')
def warehouse():
    context = get_context()
    return render_template('warehouse.html', **context)


@app.route('/add_product', methods=['POST'])
def add_product():
    form = AddProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data
        )
        db.session.add(product)
        db.session.commit()
        context = get_context()
        return render_template('table.html', **context)


@app.route('/add_location', methods=['POST'])
def add_location():
    form = AddLocationForm()
    if form.validate_on_submit():
        location = Location(
            name=form.name.data,
        )
        db.session.add(location)
        db.session.commit()
        context = get_context()
        return render_template('table.html', **context)


@app.route('/add_to_inventory', methods=['POST'])
def add_to_inventory():
    product_id = request.form.get('product_id')
    form = AddToInventoryForm(product_id=product_id)
    if form.validate_on_submit():
        inventory = Inventory(
            product_id=product_id,
            location_id=form.location_id.data.id,
        )
        db.session.add(inventory)
        db.session.commit()
        context = get_context()
        return render_template('table.html', **context)


@app.route('/delete_from_inventory', methods=['POST'])
def delete_from_inventory():
    product_id = request.form.get('product_id')
    form = DeleteFromInventoryForm(product_id=product_id)
    if form.validate_on_submit():
        inventory = Inventory.query.filter_by(
            product_id=product_id, location_id=form.location_id.data.id).first()
        if inventory:
            db.session.delete(inventory)
            db.session.commit()
            context = get_context()
            return render_template('table.html', **context)


@app.route('/change_quantity', methods=['POST'])
def change_quantity():
    product_id = request.form.get('product_id')
    form = ChangeQuantityForm(product_id=product_id)
    if form.validate_on_submit():
        inventory = Inventory.query.filter_by(
            product_id=product_id, location_id=form.location_id.data.id).first()
        if inventory:
            inventory.quantity = int(form.quantity.data)
            db.session.commit()
            context = get_context()
            return render_template('table.html', **context)


@app.route('/search', methods=['POST'])
def search_by_input():
    context = get_context()
    user_input = request.form.get('user_input')
    user_input_search = Product.query.filter(Product.name.contains(user_input))
    context['products'] = user_input_search
    return render_template('table.html', **context)


@app.route('/filter_by_location', methods=['POST'])
def filter_by_location():
    context = get_context()
    location = int(request.form.get('location'))
    sorting_by_location = Product.query.join(
        Inventory).filter(Inventory.location_id == location)
    context['products'] = sorting_by_location
    return render_template('table.html', **context)


@app.route('/sort_by_price_ascending')
def sort_by_price_ascending():
    context = get_context()
    sorting_by_price = Product.query.order_by(Product.price.asc())
    context['products'] = sorting_by_price
    return render_template('table.html', **context)


@app.route('/sort_by_price_descending')
def sort_by_price_descending():
    context = get_context()
    sorting_by_price = Product.query.order_by(Product.price.desc())
    context['products'] = sorting_by_price
    return render_template('table.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
