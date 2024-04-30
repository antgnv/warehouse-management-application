from flask import render_template, request
from warehouse import app
from warehouse.models import db, Product, Location, Inventory
from warehouse.forms import AddProductForm, AddLocationForm, AddToInventoryForm, DeleteFromInventoryForm, ChangeQuantityForm, FilterByLocation

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
        return render_template('warehouse.html', **context)


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
