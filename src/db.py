import psycopg2
from os import listdir, getenv


class Database:
    connection = None
    connection_args = dict(
        dbname=getenv(f"RDS_DB_NAME"),
        user=getenv(f"RDS_USERNAME"),
        password=getenv(f"RDS_PASSWORD"),
        host=getenv(f"RDS_HOST"),
        port=getenv(f"RDS_PORT")
    )

    @classmethod
    def get_cursor(cls):
        if not cls.connection:
            cls.connection = psycopg2.connect(**cls.connection_args)
        return cls.connection.cursor()

    @classmethod
    def initialize(cls):
        c = cls.get_cursor()
        for table in listdir('table_schemas'):
            with open(f'./table_schemas/{table}') as schema:
                c.execute(schema.read())
        cls.connection.commit()

    @classmethod
    def insert_into_table(cls, table, record):
        c = cls.get_cursor()
        c.execute(
            f'''INSERT INTO {table} ({tuple(record.keys())}) VALUES ({tuple(record.values())})'''
        )
        c.commit()

    @classmethod
    def update_table(cls, table, id_key, id_value, update_key, update_value):
        c = cls.get_cursor()
        c.execute(
            f'''UPDATE {table} SET {update_key} = {update_value} WHERE {id_key} = {id_value}'''
        )
        c.commit()
