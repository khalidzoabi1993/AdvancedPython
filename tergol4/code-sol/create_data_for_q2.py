import mysql.connector
import configparser

# Read configuration from the config.ini file
def get_db_config():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return {
        "host": config["mysql"]["host"],
        "user": config["mysql"]["user"],
        "password": config["mysql"]["password"],
    }


def connect_to_database():
    db_config = get_db_config()
    return mysql.connector.connect(**db_config)


def create_database():
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS music_service")
    connection.close()


def create_tables():
    db_config = get_db_config()
    connection = mysql.connector.connect(**db_config, database="music_service")
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
        CREATE TABLE IF NOT EXISTS songs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255)
        )
    """
    )
    connection.close()


def insert_sample_data():
    db_config = get_db_config()
    connection = mysql.connector.connect(**db_config, database="music_service")
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
        INSERT INTO songs (title) VALUES
        ('Song 1'),
        ('Song 2'),
        ('Song 3')
    """
    )
    connection.commit()
    connection.close()


# Call the functions to create the database, tables, and insert sample data
create_database()
create_tables()
insert_sample_data()
