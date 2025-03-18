from flask import Flask, jsonify, request
import psycopg2
from class.py import Car, add_accident
from save_load.py import save_car,load_car,save_accident,load_accident

app = Flask(__name__)

DB_HOST = '79.174.88.238'
DB_PORT = 15221
DB_NAME = 'school_db'
DB_USER = 'school'
DB_PASSWORD = 'School1234*'

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

def create_schema_and_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("CREATE SCHEMA IF NOT EXISTS igumentsev_kostromin;")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS igumentsev_kostromin.cars (
        id SERIAL PRIMARY KEY,
        model VARCHAR(100) NOT NULL,
        year INTEGER NOT NULL CHECK (year > 1885),
        color VARCHAR(50),
        number VARCHAR(20) UNIQUE NOT NULL,
        type VARCHAR(50) CHECK (type IN ('седан', 'купе', 'кроссовер', 'внедорожник', 'хэтчбек', 'универсал'))
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS igumentsev_kostromin.accidents (
        id SERIAL PRIMARY KEY,
        car_id INTEGER NOT NULL,
        date DATE NOT NULL,
        description TEXT,
        FOREIGN KEY (car_id) REFERENCES igumentsev_kostromin.cars(id) ON DELETE CASCADE
    );
    """)
    
    conn.commit()
    cursor.close()
    conn.close()

create_schema_and_tables()

@app.route('/cars', methods=['GET'])
def get_cars():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM igumentsev_kostromin.cars;")
    cars = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return jsonify(cars)

@app.route('/cars/<int:id>', methods=['GET'])
def get_car(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM igumentsev_kostromin.cars WHERE id = %s;", (id,))
    car = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return jsonify(car)

@app.route('/cars', methods=['POST'])
def add_car():
    new_car = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO igumentsev_kostromin.cars (model, year, color, number, type)
        VALUES (%s, %s, %s, %s, %s) RETURNING id;
    """, (new_car['model'], new_car['year'], new_car['color'], new_car['number'], new_car['type']))
    car_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"id": car_id, **new_car})

@app.route('/cars/<int:id>', methods=['PUT'])
def update_car(id):
    updated_car = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE igumentsev_kostromin.cars
        SET model = %s, year = %s, color = %s, number = %s, type = %s
        WHERE id = %s;
    """, (updated_car['model'], updated_car['year'], updated_car['color'], updated_car['number'], updated_car['type'], id))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"message": "Автомобиль успешно обновлен."})

@app.route('/cars/<int:id>', methods=['DELETE'])
def delete_car(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM igumentsev_kostromin.cars WHERE id = %s;", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"message": "Автомобиль успешно удален."})

@app.route('/accidents', methods=['GET'])
def get_accidents():
    car_id = request.args.get('car_id')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM igumentsev_kostromin.accidents WHERE car_id = %s;", (car_id,))
    accidents = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return jsonify(accidents)
@app.route('/accidents', methods=['POST'])
def add_accident():
    new_accident = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO igumentsev_kostromin.accidents (car_id, date, description)
        VALUES (%s, %s, %s) RETURNING id;
 """, (new_accident['car_id'], new_accident['date'], new_accident['description']))
    accident_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"id": accident_id, **new_accident})

@app.route('/accidents/<int:id>', methods=['PUT'])
def update_accident(id):
    updated_accident = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE igumentsev_kostromin.accidents
        SET date = %s, description = %s
        WHERE id = %s;
    """, (updated_accident['date'], updated_accident['description'], id))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"message": "Информация о ДТП успешно обновлена."})

@app.route('/accidents/<int:id>', methods=['DELETE'])
def delete_accident(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM igumentsev_kostromin.accidents WHERE id = %s;", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"message": "ДТП успешно удалено."})



if __name__ == 'main':
    app.run(debug=True)