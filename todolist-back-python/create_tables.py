from peewee import SqliteDatabase

from infra.peewee.sdk import SqliteSdk


def main():
    sdk = SqliteSdk(SqliteDatabase("./todolist.db.sqlite"))
    sdk.create_tables()

if __name__ == "__main__":
    main()