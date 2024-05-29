from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

DATABASE = 'ford_models.db'

def connect_db():
    conn = sqlite3.connect(DATABASE, timeout=10)  # Increased timeout
    return conn

@app.route('/create_table', methods=['GET'])
def create_table():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS ford_models')  # Drop the existing table if it exists
        cursor.execute('''
            CREATE TABLE ford_models (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_name TEXT NOT NULL,
                year INTEGER NOT NULL,
                price REAL NOT NULL,
                horsepower INTEGER NOT NULL
            )
        ''')
        conn.commit()
    return "Table created successfully"

@app.route('/populate_data', methods=['GET'])
def populate_data():
    car_data = [
        ('Mustang', 2023, 57945.0, 450),
        ('F-150', 2022, 33315.0, 290),
        ('Escape', 2021, 26800.0, 250),
        ('Explorer', 2023, 36760.0, 300),
        ('Bronco', 2023, 35000.0, 300),
        ('Escape', 2024, 29495.0, 250)
    ]

    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.executemany('''
            INSERT INTO ford_models (model_name, year, price, horsepower)
            VALUES (?, ?, ?, ?)
        ''', car_data)
        conn.commit()
    return "Data populated successfully"

@app.route('/cars', methods=['GET'])
def get_cars():
    cars = []
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM ford_models')
        rows = cursor.fetchall()
        for row in rows:
            cars.append({
                'id': row[0],
                'model_name': row[1],
                'year': row[2],
                'price': row[3],
                'horsepower': row[4]
            })
    return jsonify(cars)

@app.route('/debug_db', methods=['GET'])
def debug_db():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM ford_models')
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    return "Check the console for database contents"

@app.route('/sort_cars', methods=['GET'])
def sort_cars():
    sort_by = request.args.get('sort_by', 'price')  # Default to sorting by price
    order = request.args.get('order', 'asc')  # Default to ascending order

    cars = []
    with connect_db() as conn:
        cursor = conn.cursor()
        if order == 'asc':
            cursor.execute(f'SELECT * FROM ford_models ORDER BY {sort_by} ASC')
        else:
            cursor.execute(f'SELECT * FROM ford_models ORDER BY {sort_by} DESC')
        rows = cursor.fetchall()
        for row in rows:
            cars.append({
                'id': row[0],
                'model_name': row[1],
                'year': row[2],
                'price': row[3],
                'horsepower': row[4]
            })

    return jsonify(cars)

if __name__ == '__main__':
    app.run(debug=True)
