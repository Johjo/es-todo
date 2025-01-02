import sqlite3

def migrate_to_actual(connection: sqlite3.Connection):
    pass

def main():
    database = sqlite3.connect("./todolist.db.sqlite")
    migrate_to_actual(database)


if __name__ == "__main__":
    main()
