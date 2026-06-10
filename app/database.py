import mysql.connector

class Database:
    def __init__(self, config):
        self._config = config

    def get_connection(self):
        return mysql.connector.connect(
            host=self._config.db_host,
            user=self._config.db_user,
            password=self._config.db_password,
            database=self._config.db_name,
        )
