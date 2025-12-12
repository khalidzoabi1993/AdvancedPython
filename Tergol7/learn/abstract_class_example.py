from abc import ABC, abstractmethod

# Interface
class Flyable(ABC):
    @abstractmethod
    def fly(self):
        pass

# Abstract Class
class Vehicle(ABC):
    def __init__(self, brand):
        self.brand = brand

    @abstractmethod
    def move(self):
        pass

# Concrete classes
class Car(Vehicle):
    def move(self):
        return "Driving"

class Plane(Vehicle, Flyable):
    def move(self):
        return "Flying forward"

    def fly(self):
        return "Ascending..."
