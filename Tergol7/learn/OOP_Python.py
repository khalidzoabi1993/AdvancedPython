class Employee:
    def __init__(self, name):
        self.name = name

    def salary(self):
        return 0
class Manager(Employee):
    def salary(self):
        return 20000
class Developer(Employee):
    def salary(self):
        return 15000
class Intern(Employee):
    def salary(self):
        return 5000

team = [
    Manager("Noa"),
    Developer("Khaled"),
    Intern("Ward")
]

for emp in team:
    print(emp.name, emp.salary())
