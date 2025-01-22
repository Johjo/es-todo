import os
import sqlite3

from dotenv import load_dotenv

from infra.sqlite.sdk import SqliteSdk


def main():
    load_dotenv()
    database_path = os.environ["DATABASE_PATH"]
    print(f"*****Create tables for {database_path}*****")

    sdk = SqliteSdk(sqlite3.connect(database_path))
    sdk.create_tables()

if __name__ == "__main__":
    main()