from solution.vehicles.Vehicle import Vehicle


class Plane(Vehicle):
    def __init__(self, brand, year, engines):
        super().__init__(brand, year)
        self.engines = engines

    def move(self):
        return f"Plane is flying with {self.engines} engines"