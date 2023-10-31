import sqlite3

from django.db import transaction


class MyFileManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()


class MyAtomicTransaction:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_path)
        self.connection.execute("BEGIN TRANSACTION")
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.connection.execute("COMMIT")
        else:
            self.connection.execute("ROLLBACK")
        self.connection.close()


def test_context_atomic_transaction():
    # Using the 'with' statement and the AtomicTransaction context manager
    db_path = 'users.db'
    with MyAtomicTransaction(db_path) as db:
        try:
            # Operations within the transaction
            cursor = db.cursor()
            cursor.execute("INSERT INTO users (name) VALUES ('Bob')")
            cursor.execute("UPDATE accounts SET balance = balance - 50 WHERE user_id = 1")
        except Exception as e:
            # Any exception will trigger a rollback
            print(f"Error: {e}")


def test_context_file():
    # Using the context manager with the 'with' statement
    with MyFileManager('example.txt', 'w') as file:
        file.write('Hello, context manager!')
    # File is automatically closed outside the 'with' block
