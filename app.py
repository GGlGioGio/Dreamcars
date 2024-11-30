from flask import Flask, render_template, request, redirect, url_for, session
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'secret_key'
swagger = Swagger(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    three_d_model = db.Column(db.String(500), nullable=False)

with app.app_context():
    db.create_all()

    if Car.query.count() == 0:
        cars_data = [
            {"name": "Mercedes W140 S600 V12 armored", "price": "$76,000", "image": "MercedesW140.jpg", "description": "A timeless luxury sedan, the Mercedes W140 S600 combines unmatched comfort with raw power, courtesy of its 6.0L V12 engine.", "three_d_model": "https://sketchfab.com/models/ad9650076f4c491eb90d65ccb1378b9a/embed"},
            {"name": "Mercedes Benz G-class", "price": "$141,000", "image": "MercedecG.jpg", "description": "An icon of rugged sophistication, the Mercedes-Benz G-Class blends off-road capability with luxury refinement.", "three_d_model": "https://sketchfab.com/models/93c823b00afb48538f748ba1518c9ca4/embed"},
            {"name": "BMW E38", "price": "$15,999", "image": "bmwE38.jpg", "description": "A masterpiece of executive luxury, the BMW E38 redefines driving pleasure.", "three_d_model": "https://sketchfab.com/models/e21870678bea4ab4a36796aa7f3c68df/embed"},
            {"name": "BMW M5", "price": "$120,999", "image": "bmwm5.png", "description": "The ultimate sports sedan, the BMW M5 delivers breathtaking performance with precision engineering.", "three_d_model": "https://sketchfab.com/models/cb9d2b4972e746268a82f3106a7a9154/embed"},
            {"name": "Audi RS6", "price": "$174,999", "image": "audirs6.png", "description": "The Audi RS6 is the epitome of versatility and performance, combining the practicality of a wagon with the heart of a high-performance sports car.", "three_d_model": "https://sketchfab.com/models/0486a4dcf674496b9873b4ae12c9759d/embed"},
            {"name": "Audi Q7", "price": "$100,000", "image": "audiq7.png", "description": "Sophisticated and versatile, the Audi Q7 is a luxury SUV designed for every journey.", "three_d_model": "https://sketchfab.com/models/8a47a3195b6446d581b3c657ef0448ac/embed"}
        ]
        for car_data in cars_data:
            car = Car(**car_data)
            db.session.add(car)
        db.session.commit()

@app.route('/')
def home():
    cars = Car.query.all()
    return render_template('home.html', cars=cars)

@app.route('/car/<int:id>', methods=['GET'])
def car_details(id):
    car = Car.query.get(id)
    if car is None:
        return render_template('404.html')
    return render_template('car_details.html', car=car)

@app.route('/car/<int:car_id>/add_to_wishlist', methods=['POST'])
def add_to_wishlist(car_id):
    car = Car.query.get(car_id)
    if car:
        if 'wishlist' not in session:
            session['wishlist'] = []

        existing_car = next((item for item in session['wishlist'] if item['id'] == car_id), None)
        if existing_car:
            existing_car['quantity'] += 1
        else:
            car_copy = {
                'id': car.id,
                'name': car.name,
                'price': car.price,
                'image': car.image,
                'description': car.description,
                'three_d_model': car.three_d_model,
                'quantity': 1
            }
            session['wishlist'].append(car_copy)
            
        session.modified = True
    return redirect(url_for('wishlist'))

@app.route('/wishlist')
def wishlist():
    return render_template('wishlist.html', wishlist=session.get('wishlist', []))

@app.route('/wishlist/<int:car_id>/remove', methods=['POST'])
def remove_from_wishlist(car_id):
    if 'wishlist' in session:
        car = next((item for item in session['wishlist'] if item['id'] == car_id), None)
        if car:
            if 'quantity' not in car:
                car['quantity'] = 1
            
            if car['quantity'] > 1:
                car['quantity'] -= 1
            else:
                session['wishlist'] = [item for item in session['wishlist'] if item['id'] != car_id]
            session.modified = True
    return redirect(url_for('wishlist'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)