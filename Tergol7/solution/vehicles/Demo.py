from solution.vehicles.Car import Car
from solution.vehicles.Bike import Bike
from solution.vehicles.Plane import Plane


def demo(vehicles):
    for v in vehicles:
        print("Brand:", v.brand)
        print("Action:", v.move())
        print("---")


if __name__ == "__main__":
    car = Car("Toyota", 2020, 5)
    bike = Bike("Giant", 2022, True)
    plane = Plane("Boeing", 2018, 2)

    vehicles_list = [car, bike, plane]
    demo(vehicles_list)