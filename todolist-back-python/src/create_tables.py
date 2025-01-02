import sqlite3

from infra.sqlite.sdk import SqliteSdk


def main():
    sdk = SqliteSdk(sqlite3.connect("/db/todolist.db.sqlite"))
    sdk.create_tables()

if __name__ == "__main__":
    main()