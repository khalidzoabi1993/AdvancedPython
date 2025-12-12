"""
Question 1:

Create a Python program that models a movie rental system using classes and inheritance. Assume you have two types of users: customers and employees. Both customers and employees can rent movies from the rental store. Implement the following:

A parent class called User with attributes name and id.
Two subclasses, Customer and Employee, each inheriting from the User class. The Customer subclass should have an additional attribute customer_id, and the Employee subclass should have an additional attribute employee_id.
A class called RentalStore which keeps track of the movies available and rented by users. Include methods to rent and return movies.
Connect your Python program with a MySQL database to store information about users and movies. Implement functions to retrieve user details and movie availability from the database.

"""

# Solution:
import mysql.connector


class User:
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id


class Customer(User):
    def __init__(self, name, user_id, customer_id):
        super().__init__(name, user_id)
        self.customer_id = customer_id


class Employee(User):
    def __init__(self, name, user_id, employee_id):
        super().__init__(name, user_id)
        self.employee_id = employee_id


class RentalStore:
    def __init__(self):
        self.movies = []

    def rent_movie(self, user, movie):
        if movie in self.movies:
            self.movies.remove(movie)
            print(f"{user.name} has rented {movie}")
        else:
            print("Sorry, the movie is not available.")

    def return_movie(self, user, movie):
        self.movies.append(movie)
        print(f"{user.name} has returned {movie}")


def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin",
        database="movie_rental",
    )


def retrieve_user_details(user_id):
    db = connect_to_database()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user_data = cursor.fetchone()
    db.close()
    return user_data


def check_movie_availability(movie):
    db = connect_to_database()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM movies WHERE title=%s", (movie,))
    movie_data = cursor.fetchone()
    db.close()
    if movie_data:
        return True
    else:
        return False


# Example usage:
customer1 = Customer("Alice", 1, 1001)
employee1 = Employee("Bob", 2, 2001)
rental_store = RentalStore()
rental_store.movies = ["The Shawshank Redemption", "The Godfather", "The Dark Knight"]

movie_to_rent = "The Shawshank Redemption"
if check_movie_availability(movie_to_rent):
    rental_store.rent_movie(customer1, movie_to_rent)
else:
    print("Movie not available.")

movie_to_return = "The Shawshank Redemption"
rental_store.return_movie(customer1, movie_to_return)


"""
Question 2:

Extend the previous program to include functionality for adding new movies to the rental store. Implement the following:

Modify the RentalStore class to include a method called add_movie which allows the employees to add new movies to the rental store.
Create a new class called Manager which inherits from the Employee class. This class should have an additional method called add_movie_to_store.
Connect the program with a MySQL database to store information about the movies in the rental store. Implement a function to add new movies to the database.
"""


class Manager(Employee):
    def __init__(self, name, user_id, employee_id):
        super().__init__(name, user_id, employee_id)

    def add_movie_to_store(self, movie):
        db = connect_to_database()
        cursor = db.cursor()
        cursor.execute("INSERT INTO movies (title) VALUES (%s)", (movie,))
        db.commit()
        db.close()
        print(f"{movie} has been added to the rental store.")


class RentalStore:
    def __init__(self):
        self.movies = []

    def rent_movie(self, user, movie):
        if movie in self.movies:
            self.movies.remove(movie)
            print(f"{user.name} has rented {movie}")
        else:
            print("Sorry, the movie is not available.")

    def return_movie(self, user, movie):
        self.movies.append(movie)
        print(f"{user.name} has returned {movie}")

    def add_movie(self, manager, movie):
        manager.add_movie_to_store(movie)


# Example usage:
manager1 = Manager("Charlie", 3, 3001)
rental_store = RentalStore()
rental_store.movies = ["The Shawshank Redemption", "The Godfather", "The Dark Knight"]

new_movie = "Inception"
rental_store.add_movie(manager1, new_movie)
