import mysql.connector

from create_data_for_tergol_5 import get_db_config, create_database, create_tables, insert_sample_data


# q1
def print_all_users():
    db_config = get_db_config()
    connection = mysql.connector.connect(**db_config, database="music_service")
    cursor = connection.cursor()

    cursor.execute("SELECT id, name, user_id FROM users")
    rows = cursor.fetchall()

    for row in rows:
        id_, name, user_id = row
        print(f"ID: {id_} | Name: {name} | User ID: {user_id}")

    connection.close()

# q2
def get_user_by_user_id(user_id):
    db_config = get_db_config()
    connection = mysql.connector.connect(**db_config, database="music_service")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE user_id = %s",
        (user_id,)
    )

    row = cursor.fetchone()

    if row is None:
        print(f"User with user_id {user_id} not found")
        connection.close()
        return None
    else:
        id_, name, user_id = row
        print(f"Found user -> ID: {id_} | Name: {name} | User ID: {user_id}")
        connection.close()
        return row

# q3
def add_user(name, user_id):
    db_config = get_db_config()
    connection = mysql.connector.connect(**db_config, database="music_service")
    cursor = connection.cursor()

    # בדיקה אם user_id כבר קיים
    cursor.execute(
        "SELECT id FROM users WHERE user_id = %s",
        (user_id,)
    )
    existing = cursor.fetchone()

    if existing is not None:
        print(f"User with user_id {user_id} already exists")
        connection.close()
        return

    # הוספת המשתמש
    cursor.execute(
        "INSERT INTO users (name, user_id) VALUES (%s, %s)",
        (name, user_id)
    )
    connection.commit()
    print(f"User {name} with user_id {user_id} added successfully")

    connection.close()

# q4
def update_user_name(user_id, new_name):
    db_config = get_db_config()
    connection = mysql.connector.connect(**db_config, database="music_service")
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE users SET name = %s WHERE user_id = %s",
        (new_name, user_id)
    )
    connection.commit()

    if cursor.rowcount == 0:
        print(f"No user found with user_id {user_id}")
    else:
        print(f"User with user_id {user_id} updated to name {new_name}")

    connection.close()


# q5
def delete_user(user_id):
    db_config = get_db_config()
    connection = mysql.connector.connect(**db_config, database="music_service")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM users WHERE user_id = %s",
        (user_id,)
    )
    connection.commit()

    if cursor.rowcount == 0:
        print(f"No user found with user_id {user_id}")
    else:
        print(f"User with user_id {user_id} deleted")

    connection.close()

# q6
def print_all_songs_ordered():
    db_config = get_db_config()
    connection = mysql.connector.connect(**db_config, database="music_service")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, title FROM songs ORDER BY title ASC"
    )
    rows = cursor.fetchall()

    for row in rows:
        song_id, title = row
        print(f"Song ID: {song_id} | Title: {title}")

    connection.close()


# q7
def create_user_songs_table():
    db_config = get_db_config()
    connection = mysql.connector.connect(**db_config, database="music_service")
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user_songs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            song_id INT
        )
        """
    )

    connection.commit()
    connection.close()


def add_song_to_user(user_id, song_id):
    db_config = get_db_config()
    connection = mysql.connector.connect(**db_config, database="music_service")
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO user_songs (user_id, song_id) VALUES (%s, %s)",
        (user_id, song_id)
    )
    connection.commit()

    print(f"Song {song_id} added to user {user_id}")

    connection.close()


def print_songs_for_user(user_id):
    db_config = get_db_config()
    connection = mysql.connector.connect(**db_config, database="music_service")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT s.id, s.title
        FROM user_songs us
        JOIN songs s ON us.song_id = s.id
        WHERE us.user_id = %s
        """,
        (user_id,)
    )

    rows = cursor.fetchall()

    print(f"Songs for user_id {user_id}:")
    if len(rows) == 0:
        print("No songs found for this user")
    else:
        for row in rows:
            song_id, title = row
            print(f"- ({song_id}) {title}")

    connection.close()

#q8
def print_users_with_song_count():
    db_config = get_db_config()
    connection = mysql.connector.connect(**db_config, database="music_service")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT u.name, u.user_id, COUNT(us.song_id) AS song_count
        FROM users u
        LEFT JOIN user_songs us
            ON u.user_id = us.user_id
        GROUP BY u.id, u.name, u.user_id
        ORDER BY u.user_id
        """
    )

    rows = cursor.fetchall()

    for row in rows:
        name, user_id, count = row
        print(f"Name: {name} | user_id: {user_id} | Songs: {count}")

    connection.close()

if __name__ == "__main__":
    create_database()
    create_tables()
    insert_sample_data()
    create_user_songs_table()

    print("=== All users ===")
    print_all_users()

    # print("\n=== Get user by user_id 1 ===")
    # get_user_by_user_id(1)
    #
    # print("\n=== Add user ===")
    # add_user("David", 4)
    # print_all_users()
    #
    # print("\n=== Update user name ===")
    # update_user_name(2, "Bobby")
    # print_all_users()
    #
    # print("\n=== Delete user 3 ===")
    # delete_user(3)
    # print_all_users()
    #
    # print("\n=== Songs ordered ===")
    # print_all_songs_ordered()
    #
    # print("\n=== Add songs to users ===")
    # add_song_to_user(1, 1)
    # add_song_to_user(1, 2)
    # add_song_to_user(2, 3)
    #
    # print("\n=== Songs for user 1 ===")
    # print_songs_for_user(1)
    #
    # print("\n=== Users with song count ===")
    # print_users_with_song_count()
    #


# print_all_users()