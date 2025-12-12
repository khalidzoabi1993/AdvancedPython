class Animal:
    def __init__(self, name):
        # use the setter so validation will happen here as well
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, v):
        if len(v) < 2:
            raise ValueError("Name too short")
        self._name = v

    def speak(self):
        return "Some sound"


class Dog(Animal):
    def speak(self):
        return "Woof!"


class Cat(Animal):
    def speak(self):
        return "Meow!"


# Polymorphism demo
pets = [
    Dog("Buddy"),
    Cat("Whiskers")
]

for pet in pets:
    print(pet.name, "->", pet.speak())

# Testing the setter with validation
try:
    bad_pet = Dog("A")  # will raise now, because __init__ uses setter
except ValueError as e:
    print("Error creating pet:", e)

# Changing the name using the setter
good_pet = Cat("Mittens")
print("Before:", good_pet.name)
good_pet.name = "Fluffy"
print("After:", good_pet.name)
