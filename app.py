from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/warehouse'

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
    quantity = db.Column(db.Integer, nullable=False)

    product = db.relationship(
        'Product', backref=db.backref('inventories', lazy='dynamic'))
    location = db.relationship(
        'Location', backref=db.backref('inventories', lazy='dynamic'))


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)


@app.route('/add_product', methods=['POST'])
def add_product():
    name = request.form.get('name')
    description = request.form.get('description')
    price = float(request.form.get('price'))

    product = Product(name=name, description=description, price=price)
    db.session.add(product)
    db.session.commit()

    return jsonify({'success': True})


@app.route('/add_location', methods=['POST'])
def add_location():
    name = request.form.get('name')

    location = Location(name=name)
    db.session.add(location)
    db.session.commit()

    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True)
