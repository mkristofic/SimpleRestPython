from connector import Connector as c
import hashlib


class Auth:
    @staticmethod
    def check(username, password):
        pass_hash = hashlib.sha256(str.encode(password)).hexdigest()
        c.cursor.execute(f"select * from users where username = '{username}' and password = '{pass_hash}'")
        records = c.cursor.fetchall()
        return len(records) == 1
