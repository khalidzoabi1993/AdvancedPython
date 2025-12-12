"""
Create a Python program that models a music streaming service using classes and inheritance. Assume you have two types of users: regular users and premium users. Both types of users can listen to music from the streaming service. Implement the following:
1. A parent class called User with attributes name and id.
2. Two subclasses, RegularUser and PremiumUser, each inheriting from the User class. The RegularUser subclass should have an additional attribute membership_level set to "regular", and the PremiumUser subclass should have an additional attribute membership_level set to "premium".
3. A class called MusicService which keeps track of the available songs and playlists. Include methods to play songs and create playlists.
4. Connect your Python program with a MySQL database to store information about users, songs, and playlists. Implement functions to retrieve user details, song availability, and playlist information from the database.

"""

import mysql.connector


class User:
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id


class RegularUser(User):
    def __init__(self, name, user_id):
        super().__init__(name, user_id)
        self.membership_level = "regular"


class PremiumUser(User):
    def __init__(self, name, user_id):
        super().__init__(name, user_id)
        self.membership_level = "premium"


class MusicService:
    def __init__(self):
        self.songs = []
        self.playlists = []

    def play_song(self, user, song):
        if song in self.songs:
            print(f"{user.name} is listening to {song}")
        else:
            print("Sorry, the song is not available.")

    def create_playlist(self, user, playlist_name):
        self.playlists.append({playlist_name: []})
        print(f"{user.name} has created a playlist named {playlist_name}")


def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin",
        database="music_service",
    )


def check_song_availability(song):
    db = connect_to_database()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM songs WHERE title=%s", (song,))
    song_data = cursor.fetchone()
    db.close()
    if song_data:
        return True
    else:
        return False


# Example usage:
regular_user1 = RegularUser("Alice", 1)
premium_user1 = PremiumUser("Bob", 2)
music_service = MusicService()

song_to_play = "Song 1"
music_service.play_song(regular_user1, song_to_play)

playlist_name = "My Playlist"
music_service.create_playlist(premium_user1, playlist_name)


"""
Extend the previous program to include functionality for adding new songs to the music streaming service. Implement the following:
1. Modify the MusicService class to include a method called add_song which allows adding new songs to the available songs list.
2. Create a new class called Admin which inherits from the User class. This class should have an additional method called add_song_to_service.
3. Connect the program with a MySQL database to store information about the songs. Implement a function to add new songs to the database.

"""

import mysql.connector


class Admin(User):
    def __init__(self, name, user_id):
        super().__init__(name, user_id)

    def add_song_to_service(self, song):
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO songs (title) VALUES (%s)", (song,))
        connection.commit()
        connection.close()
        print(f"{song} has been added to the music service.")


class MusicService:
    def __init__(self):
        self.songs = []

    def play_song(self, user, song):
        if song in self.songs:
            print(f"{user.name} is listening to {song}")
        else:
            print("Sorry, the song is not available.")

    def create_playlist(self, user, playlist_name):
        print(f"{user.name} has created a playlist named {playlist_name}")

    def add_song(self, admin, song):
        self.songs.append(song)
        admin.add_song_to_service(song)


# Example usage:
admin1 = Admin("Charlie", 3)
music_service = MusicService()

new_song = "New Song"
music_service.add_song(admin1, new_song)
