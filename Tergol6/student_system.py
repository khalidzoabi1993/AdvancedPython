# file: student_system.py

from sqlalchemy import (
    Table, Column, Integer, String, Float,
    ForeignKey, select, insert, update, delete
)

from db_base import metadata, engine, create_all_tables, get_connection


# ==============================
# 1. Table Definitions
#    students, courses, enrollments
# ==============================

# TODO: Define the students table here
# students = Table(
#     "students",
#     metadata,
#     Column(...),
#     ...
# )

# TODO: Define the courses table here

# TODO: Define the enrollments table here


# ==============================
# 2. Helper Functions
#    insert_sample_data(), show_all_students(), ...
# ==============================

def create_tables():
    """
    Creates all tables in the database using metadata.
    """
    # TODO: Call the correct function from db_base
    pass


def insert_sample_data():
    """
    Inserts sample data into:
    students, courses, enrollments
    """
    # TODO: Use insert(...) and get_connection()
    pass


def show_all_students():
    """
    Prints all students from the students table.
    """
    # TODO: Use select(students)
    pass


def show_all_courses():
    """
    Prints all courses from the courses table.
    """
    # TODO: Use select(courses)
    pass


def show_enrollments_with_names():
    """
    Prints all enrollments:
    Student Name, Course Name, Grade
    (Use JOIN or multiple queries – based on instructor instructions)
    """
    # TODO: Implement according to the assignment
    pass


def update_grade(student_name, course_name, new_grade):
    """
    Updates the grade of a student in a specific course.
    """
    # TODO: Implement using update(enrollments) and where(...)
    pass


def delete_student_by_name(student_name):
    """
    Deletes a student by name (and optionally all related enrollments).
    """
    # TODO: Implement using delete(...)
    pass


# ==============================
# 3. Main Flow Example
# ==============================

def main():
    # Create tables in the database
    create_tables()

    # Insert initial sample data
    insert_sample_data()

    # Display data
    show_all_students()
    show_all_courses()
    show_enrollments_with_names()

    # Test update and delete
    update_grade("Alice", "Databases", 100)
    delete_student_by_name("Bob")


if __name__ == "__main__":
    main()
