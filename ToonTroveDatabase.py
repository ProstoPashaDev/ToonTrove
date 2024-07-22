from configparser import ConfigParser
import psycopg2


class ToonTroveDatabase:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.dbconfig_path = "database.ini"
        self.section = "postgresql"
        

    def load_config(self):
        parser = ConfigParser()
        parser.read(self.dbconfig_path)

        config = {}
        params = parser.items(self.section)
        for param in params:
            config[param[0]] = param[1]
        return config

    def connect(self, config):
        try:
            self.connection = psycopg2.connect(**config)
            self.cursor = self.connection.cursor()
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)


    def insert_new_user(self, username):
        self.cursor.execute(
            'INSERT INTO user_info (username, ttc, points, time_getcard, attempts, time_game, squad_name, collection) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
            (username, 0, 0, 0, 0, 0, None, ["1_1.jpg"]))

        self.connection.commit()


    def select_user_info(self, username):
        self.cursor.execute("SELECT * from user_info WHERE username = %s", (username, ))
        return self.cursor.fetchall()

    def check_user(self, username):
        #self.cursor.execute( "SELECT username from user_info WHERE username = %s", (username))
        self.cursor.execute("SELECT EXISTS(SELECT username FROM user_info WHERE username = %s)", (username,))
        return self.cursor.fetchone()[0]

    def close_connection(self):
        self.connection.close()
        self.cursor.close()

    def get_attempts(self, username):
        return self.select_user_info(username)[0][4]

    def get_time_getcard(self, username):
        return self.select_user_info(username)[0][3]

    def update_getcard(self, username, attempts, time):
        self.cursor.execute("UPDATE user_info SET time_getcard = %s, attempts = %s WHERE username = %s", (time, attempts-1, username))
        self.connection.commit()

    def check_attempt(self, username, time, attempt_time):
        return time - self.get_time_getcard(username) >= attempt_time

    def update_ttc_points(self, username, ttc, points):
        user_data = self.select_user_info(username)[0]
        ttc_current, points_current = int(user_data[1]), int(user_data[2])
        self.cursor.execute("UPDATE user_info SET ttc = %s, points = %s WHERE username = %s",
                            (ttc_current+ttc, points_current+points, username))
        self.connection.commit()


