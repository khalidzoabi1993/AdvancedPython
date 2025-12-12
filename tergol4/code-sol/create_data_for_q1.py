import mysql.connector
import configparser
from pathlib import Path
# Read configuration from the config.ini file
def get_db_config():

    return {
        "host": "localhost",
        "user": "root",
        "password": "admin",
    }


def create_database():
    db_config = get_db_config()
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS movie_rental")
    connection.close()


def create_tables():
    db_config = get_db_config()
    connection = mysql.connector.connect(**db_config, database="movie_rental")
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            user_id INT
        )
    """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS movies (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255)
        )
    """
    )
    connection.close()


def insert_sample_data():
    db_config = get_db_config()
    connection = mysql.connector.connect(**db_config, database="movie_rental")
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO users (name, user_id) VALUES
        ('Alice', 1),
        ('Bob', 2),
        ('Charlie', 3)
    """
    )
    cursor.execute(
        """
        INSERT INTO movies (title) VALUES
        ('The Shawshank Redemption'),
        ('The Godfather'),
        ('The Dark Knight')
    """
    )
    connection.commit()
    connection.close()


# Call the functions to create the database, tables, and insert sample data
create_database()
create_tables()
insert_sample_data()
