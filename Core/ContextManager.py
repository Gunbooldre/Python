"""
Creating Content Manager
"""


class DataBaseClass:
    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        print(f"Connection to DB {self.db_name}")
        self.connection = 'Connected'
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Exit from DB")
        self.connection = None
        return False


with DataBaseClass("test_db") as con:
    print(f"Conecting started {con} ")
