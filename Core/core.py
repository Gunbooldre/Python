"""
Creating Content Manager
"""


class DataBaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        print(f'Connecting to database {self.db_name}')
        self.connection = f'Connection to {self.db_name}'
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f'Closing a connection {self.db_name}')
        self.connection = None
        return False


with DataBaseConnection('testDB') as conn:
    print(f'Using {conn} to execute ')

