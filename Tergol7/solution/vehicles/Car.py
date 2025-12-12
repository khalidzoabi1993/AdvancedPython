from solution.vehicles.Vehicle import Vehicle


class Car(Vehicle):
    def __init__(self, brand, year, seats):
        super().__init__(brand, year)
        self.seats = seats

    def move(self):
        return f"Car is driving with {self.seats} seats"