from peewee import DateField, Database, SqliteDatabase, CharField, IntegerField  # type: ignore
from playhouse.migrate import SqliteMigrator, migrate  # type: ignore

def migrate_to_actual(database: Database):
    # migrator = SqliteMigrator(database)
    migrate(
    )



def main():
    path = "./todolist.db.sqlite"
    database = SqliteDatabase(path)
    migrate_to_actual(database)

if __name__ == "__main__":
    main()
