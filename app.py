from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'secret_key'

cars = [
    {"id": 1, "name": "Mercedes W140 S600 V12 armored", "price": "$76,000", "image": "MercedesW140.jpg", "description": "A timeless luxury sedan, the Mercedes W140 S600 combines unmatched comfort with raw power, courtesy of its 6.0L V12 engine. Its armored configuration elevates it to a fortress on wheels, offering supreme safety without compromising elegance or performance.", "3d_model": "https://sketchfab.com/models/ad9650076f4c491eb90d65ccb1378b9a/embed"},
    {"id": 2, "name": "Mercedes Benz G-class", "price": "$141,000", "image": "MercedecG.jpg", "description": "An icon of rugged sophistication, the Mercedes-Benz G-Class blends off-road capability with luxury refinement. Its bold design, all-terrain prowess, and premium interior make it a symbol of power and prestige.", "3d_model": "https://sketchfab.com/models/93c823b00afb48538f748ba1518c9ca4/embed"},
    {"id": 3, "name": "BMW E38", "price": "$15,999", "image": "bmwE38.jpg", "description": "A masterpiece of executive luxury, the BMW E38 redefines driving pleasure with its graceful design, advanced technology, and dynamic performance. It’s a true testament to BMW’s commitment to innovation and elegance.", "3d_model": "https://sketchfab.com/models/e21870678bea4ab4a36796aa7f3c68df/embed"},
    {"id": 4, "name": "BMW M5", "price": "$120,999", "image": "bmwm5.png", "description": "The ultimate sports sedan, the BMW M5 delivers breathtaking performance with precision engineering. Its aggressive styling and adrenaline-inducing power make it a legend on both road and track.", "3d_model": "https://sketchfab.com/models/cb9d2b4972e746268a82f3106a7a9154/embed"},
    {"id": 5, "name": "Audi RS6", "price": "$174,999", "image": "audirs6.png", "description": "The Audi RS6 is the epitome of versatility and performance, combining the practicality of a wagon with the heart of a high-performance sports car. Its striking design and blistering speed make it a true icon.", "3d_model": "https://sketchfab.com/models/0486a4dcf674496b9873b4ae12c9759d/embed"},
    {"id": 6, "name": "Audi Q7", "price": "$100,000", "image": "audiq7.png", "description": "Sophisticated and versatile, the Audi Q7 is a luxury SUV designed for every journey. With advanced technology, premium comfort, and confident handling, it embodies the perfect balance of style and substance.", "3d_model": "https://sketchfab.com/models/8a47a3195b6446d581b3c657ef0448ac/embed"}
]

@app.route('/')
def home():
    return render_template('home.html', cars=cars)

@app.route('/car/<int:id>', methods=['GET'])
def car_details(id):
    car = next((car for car in cars if car['id'] == id), None)
    if car is None:
        return render_template('404.html')
    return render_template('car_details.html', car=car)

@app.route('/car/<int:car_id>/add_to_wishlist', methods=['POST'])
def add_to_wishlist(car_id):
    car = next((car for car in cars if car['id'] == car_id), None)
    if car:
        if 'wishlist' not in session:
            session['wishlist'] = []

        existing_car = next((item for item in session['wishlist'] if item['id'] == car_id), None)
        if existing_car:
            existing_car['quantity'] += 1
        else:
            car_copy = car.copy()
            car_copy['quantity'] = 1
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
    app.run(debug=True)
