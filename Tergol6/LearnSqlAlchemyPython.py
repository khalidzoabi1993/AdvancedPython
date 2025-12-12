# file: db_core_demo.py

import configparser
from sqlalchemy import (
    create_engine, MetaData, Table, Column,
    Integer, String, select, insert, update, delete, text
)

# ---------- קריאת הגדרות החיבור מתוך config.ini ----------

def get_db_config():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return {
        "host": config["mysql"]["host"],
        "user": config["mysql"]["user"],
        "password": config["mysql"]["password"],
    }


DB_NAME = "khalid_service"

db = get_db_config()

# חיבור לשרת MySQL בלי מסד נתונים (ליצירת ה-DB)
SERVER_URL = f"mysql+pymysql://{db['user']}:{db['password']}@{db['host']}"
server_engine = create_engine(SERVER_URL, echo=True, future=True)

# חיבור למסד הנתונים (נשתמש בו אחרי שניצור את ה-DB)
DB_URL = f"mysql+pymysql://{db['user']}:{db['password']}@{db['host']}/{DB_NAME}"
engine = create_engine(DB_URL, echo=True, future=True)

# ---------- הגדרת מבנה הטבלאות עם SQLAlchemy Core ----------

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255)),
    Column("user_id", Integer),
)

songs = Table(
    "songs",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(255)),
)

# ---------- פונקציות עבודה ----------

def create_database():
    """יוצר מסד נתונים אם לא קיים."""
    with server_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
        print(f"Database '{DB_NAME}' created (or already exists).")


def create_tables():
    """יוצר את הטבלאות users ו-songs אם לא קיימות."""
    metadata.create_all(engine)
    print("Tables 'users' and 'songs' created (or already exist).")


def insert_sample_data():
    """מכניס נתוני דוגמה לטבלאות."""
    with engine.begin() as conn:
        # הוספת משתמשים
        stmt_users = insert(users)
        conn.execute(
            stmt_users,
            [
                {"name": "Alice", "user_id": 1},
                {"name": "Bob", "user_id": 2},
                {"name": "Charlie", "user_id": 3},
            ],
        )

        # הוספת שירים
        stmt_songs = insert(songs)
        conn.execute(
            stmt_songs,
            [
                {"title": "Song 1"},
                {"title": "Song 2"},
                {"title": "Song 3"},
            ],
        )

        print("Sample data inserted.")


def show_all_users():
    """מדפיס את כל המשתמשים."""
    with engine.connect() as conn:
        stmt = select(users)
        result = conn.execute(stmt)

        print("All users:")
        for row in result:
            # row הוא אובייקט עם שדות לפי עמודות הטבלה
            print(row.id, row.name, row.user_id)


def show_all_songs():
    """מדפיס את כל השירים."""
    with engine.connect() as conn:
        stmt = select(songs)
        result = conn.execute(stmt)

        print("All songs:")
        for row in result:
            print(row.id, row.title)


def show_users_with_high_id():
    """מדפיס משתמשים עם user_id גדול מ-1."""
    with engine.connect() as conn:
        stmt = select(users).where(users.c.user_id > 1)
        result = conn.execute(stmt)

        print("Users with user_id > 1:")
        for row in result:
            print(row.id, row.name, row.user_id)


def update_user_id_for_alice():
    """מעדים את ה-user_id של Alice ל-99."""
    with engine.begin() as conn:
        stmt = (
            update(users)
            .where(users.c.name == "Alice")
            .values(user_id=99)
        )
        conn.execute(stmt)
        print("Alice's user_id updated to 99.")


def delete_user_bob():
    """מוחק את המשתמש Bob."""
    with engine.begin() as conn:
        stmt = delete(users).where(users.c.name == "Bob")
        conn.execute(stmt)
        print("User 'Bob' deleted.")


# ---------- נקודת כניסה לתוכנית ----------

def main():
    create_database()
    create_tables()
    insert_sample_data()

    show_all_users()
    show_all_songs()

    show_users_with_high_id()

    update_user_id_for_alice()
    delete_user_bob()

    print("\nAfter update & delete:")
    show_all_users()


if __name__ == "__main__":
    main()
