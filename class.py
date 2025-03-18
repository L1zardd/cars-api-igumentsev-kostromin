class Car:
    def __init__(self, id, model, year, color, number, type):
        self.id = id
        self.model = model
        self.year = year
        self.color = color
        self.number = number
        self.type = type

    def to_dict(self):
        return {
            "id": self.id,
            "model": self.model,
            "year": self.year,
            "color": self.color,
            "number": self.number,
            "type": self.type
        }

class Accident:
    def __init__(self, id, car_id, date, description):
        self.id = id
        self.car_id = car_id
        self.date = date
        self.description = description

    def to_dict(self):
        return {
            "id": self.id,
            "car_id": self.car_id,
            "date": str(self.date),
            "description": self.description
        }
