# file: student_system.py

from sqlalchemy import (
    Table, Column, Integer, String, Float,
    ForeignKey, select, insert, update, delete
)

from db_base import metadata, engine, create_all_tables


# ====================================
# 1. Table Definitions
#    students, courses, enrollments
# ====================================

students = Table(
    "students",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255), nullable=False),
    Column("email", String(255), nullable=False),
    Column("year", Integer, nullable=False),
)

courses = Table(
    "courses",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255), nullable=False),
    Column("points", Float, nullable=False),
)

enrollments = Table(
    "enrollments",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("student_id", Integer, ForeignKey("students.id"), nullable=False),
    Column("course_id", Integer, ForeignKey("courses.id"), nullable=False),
    Column("grade", Float, nullable=False),
)


# ====================================
# 2. Helper Functions
# ====================================

def create_tables():
    """
    Creates all tables in the database using metadata.
    Only creates tables that do not already exist.
    """
    create_all_tables()


def insert_sample_data():
    """
    Inserts sample data into:
    students, courses, enrollments.
    Assumes the tables are empty when run the first time.
    """
    with engine.begin() as conn:
        # Insert students
        conn.execute(
            insert(students),
            [
                {"name": "Alice", "email": "alice@example.com", "year": 1},
                {"name": "Bob", "email": "bob@example.com", "year": 2},
                {"name": "Charlie", "email": "charlie@example.com", "year": 3},
            ],
        )

        # Insert courses
        conn.execute(
            insert(courses),
            [
                {"name": "Databases", "points": 4.0},
                {"name": "Python Programming", "points": 3.0},
                {"name": "Algorithms", "points": 5.0},
            ],
        )

        # For simplicity, assume IDs start at 1 and go in order
        # (as long as this runs on a fresh DB or once)
        conn.execute(
            insert(enrollments),
            [
                # Alice
                {"student_id": 1, "course_id": 1, "grade": 95},
                {"student_id": 1, "course_id": 2, "grade": 88},

                # Bob
                {"student_id": 2, "course_id": 2, "grade": 75},
                {"student_id": 2, "course_id": 3, "grade": 82},

                # Charlie
                {"student_id": 3, "course_id": 1, "grade": 90},
            ],
        )

        print("Sample data inserted.")


def show_all_students():
    """
    Prints all students from the students table.
    """
    with engine.connect() as conn:
        result = conn.execute(select(students))
        print("=== Students ===")
        for row in result:
            print(
                f"ID: {row.id}, "
                f"Name: {row.name}, "
                f"Email: {row.email}, "
                f"Year: {row.year}"
            )
        print()


def show_all_courses():
    """
    Prints all courses from the courses table.
    """
    with engine.connect() as conn:
        result = conn.execute(select(courses))
        print("=== Courses ===")
        for row in result:
            print(
                f"ID: {row.id}, "
                f"Name: {row.name}, "
                f"Points: {row.points}"
            )
        print()


def show_enrollments_with_names():
    """
    Prints all enrollments with student name, course name and grade.
    Uses JOIN between enrollments, students and courses.
    """
    from sqlalchemy import join

    j = (
        enrollments.join(students, enrollments.c.student_id == students.c.id)
                   .join(courses, enrollments.c.course_id == courses.c.id)
    )

    stmt = select(
        students.c.name.label("student_name"),
        courses.c.name.label("course_name"),
        enrollments.c.grade
    ).select_from(j)

    with engine.connect() as conn:
        result = conn.execute(stmt)
        print("=== Enrollments ===")
        for row in result:
            print(
                f"Student: {row.student_name}, "
                f"Course: {row.course_name}, "
                f"Grade: {row.grade}"
            )
        print()


def update_grade(student_name, course_name, new_grade):
    """
    Updates the grade of a given student in a given course.
    Looks up IDs by names, then updates enrollments.
    """
    with engine.begin() as conn:
        # Find student id
        student_id = conn.execute(
            select(students.c.id).where(students.c.name == student_name)
        ).scalar_one_or_none()

        if student_id is None:
            print(f"Student '{student_name}' not found.")
            return

        # Find course id
        course_id = conn.execute(
            select(courses.c.id).where(courses.c.name == course_name)
        ).scalar_one_or_none()

        if course_id is None:
            print(f"Course '{course_name}' not found.")
            return

        # Update grade
        stmt = (
            update(enrollments)
            .where(
                enrollments.c.student_id == student_id,
                enrollments.c.course_id == course_id,
            )
            .values(grade=new_grade)
        )

        result = conn.execute(stmt)

        if result.rowcount == 0:
            print(
                f"No enrollment found for student '{student_name}' "
                f"in course '{course_name}'."
            )
        else:
            print(
                f"Updated grade for '{student_name}' in '{course_name}' "
                f"to {new_grade}."
            )


def delete_student_by_name(student_name):
    """
    Deletes a student by name and all related enrollments.
    """
    with engine.begin() as conn:
        # Find student id
        student_id = conn.execute(
            select(students.c.id).where(students.c.name == student_name)
        ).scalar_one_or_none()

        if student_id is None:
            print(f"Student '{student_name}' not found.")
            return

        # Delete enrollments first (referential integrity)
        del_enrollments = delete(enrollments).where(
            enrollments.c.student_id == student_id
        )
        conn.execute(del_enrollments)

        # Delete student
        del_student = delete(students).where(students.c.id == student_id)
        conn.execute(del_student)

        print(f"Student '{student_name}' and related enrollments deleted.")


# ====================================
# 3. Main Flow Example
# ====================================

def main():
    # Create tables in the database
    create_tables()

    # Insert initial sample data
    # insert_sample_data()
    #
    # # Display data
    # show_all_students()
    # show_all_courses()
    # show_enrollments_with_names()
    #
    # # Test update and delete
    # update_grade("Alice", "Databases", 100)
    # show_enrollments_with_names()
    #
    # delete_student_by_name("Bob")
    # show_all_students()
    # show_enrollments_with_names()


if __name__ == "__main__":
    main()
