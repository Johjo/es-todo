
from peewee import DateField, Database, SqliteDatabase  # type: ignore
from playhouse.migrate import SqliteMigrator, migrate  # type: ignore

def migrate_to_actual(database: Database):
    migrator = SqliteMigrator(database)
    execution_date = DateField(null=True)
    migrate(
        migrator.add_index(table="task", columns=["todolist_name"]),
        migrator.add_column(table="task", column_name="execution_date", field=execution_date)
    )


def main():
    path = "./todolist.db.sqlite"
    database = SqliteDatabase(path)
    migrate_to_actual(database)

if __name__ == "__main__":
    main()
