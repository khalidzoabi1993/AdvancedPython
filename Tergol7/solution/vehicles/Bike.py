from solution.vehicles.Vehicle import Vehicle


class Bike(Vehicle):
    def __init__(self, brand, year, electric):
        super().__init__(brand, year)
        self.electric = electric

    def move(self):
        if self.electric:
            return "Electric bike is riding"
        else:
            return "Regular bike is riding"