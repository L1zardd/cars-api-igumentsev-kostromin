def load_car(car_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM igumentsev_kostromin.cars WHERE id = %s;", (car_id,))
    car_data = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if car_data:
        return Car(*car_data)
    return None

def save_car(car: Car):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO igumentsev_kostromin.cars (model, year, color, number, type)
        VALUES (%s, %s, %s, %s, %s) RETURNING id;
    """, (car.model, car.year, car.color, car.number, car.type))
    car_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    
    car.id = car_id
    return car

def load_accident(accident_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM igumentsev_kostromin.accidents WHERE id = %s;", (accident_id,))
    accident_data = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if accident_data:
        return Accident(*accident_data)
    return None

def save_accident(accident: Accident):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO igumentsev_kostromin.accidents (car_id, date, description)
        VALUES (%s, %s, %s) RETURNING id;
    """, (accident.car_id, accident.date, accident.description))
    accident_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    
    accident.id = accident_id
    return accident
