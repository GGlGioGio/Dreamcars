from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'secret_key'

# Примерный список автомобилей
cars = [
    {"id": 1, "name": "Mercedes W140 S600 V12 armored", "price": "$76,000", "image": "MercedesW140.jpg", "description": "Luxury armored sedan."},
    {"id": 2, "name": "Mercedes-Benz G 63 AMG BRABUS 800", "price": "$600,000", "image": "MercedecG.jpg", "description": "Powerful SUV tuned by BRABUS."},
    {"id": 3, "name": "BMW E38", "price": "$15,999", "image": "bmwE38.jpg", "description": "Classic luxury sedan."},
    {"id": 4, "name": "BMW M5", "price": "$120,999", "image": "bmwm5.png", "description": "Ultimate sports sedan."},
    {"id": 5, "name": "Audi RS6", "price": "$174,999", "image": "audirs6.png", "description": "High-performance station wagon."},
    {"id": 6, "name": "Audi Q7", "price": "$100,000", "image": "audiq7.png", "description": "Luxurious family SUV."}
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

        # Проверка, если машина уже в вишлисте
        existing_car = next((item for item in session['wishlist'] if item['id'] == car_id), None)
        if existing_car:
            # Если машина уже есть, увеличиваем количество
            existing_car['quantity'] += 1
        else:
            # Если машины нет, добавляем её в список с полем quantity
            car_copy = car.copy()  # Создаем копию машины
            car_copy['quantity'] = 1  # Устанавливаем количество 1
            session['wishlist'].append(car_copy)  # Добавляем машину в вишлист

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
            # Проверяем наличие ключа 'quantity', если его нет — устанавливаем в 1
            if 'quantity' not in car:
                car['quantity'] = 1
            
            if car['quantity'] > 1:
                # Если количество больше 1, уменьшаем на 1
                car['quantity'] -= 1
            else:
                # Если количество 1, удаляем машину
                session['wishlist'] = [item for item in session['wishlist'] if item['id'] != car_id]
            session.modified = True
    return redirect(url_for('wishlist'))

if __name__ == '__main__':
    app.run(debug=True)
