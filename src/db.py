from sqlalchemy import create_engine
from os import listdir, getenv


class Database:
    user = getenv('RDS_USERNAME')
    password = getenv('RDS_PASSWORD')
    host = getenv('RDS_HOSTNAME')
    port = getenv('RDS_PORT')
    dbname = getenv('RDS_DB_NAME')

    engine = None

    @classmethod
    def get_engine(cls):
        if not cls.engine:
            cls.engine = create_engine(
                f'mysql+pymysql://{cls.user}:{cls.password}@{cls.host}:{cls.port}/{cls.dbname}',
                pool_pre_ping=True
            )
        return cls.engine

    @classmethod
    def initialize(cls):
        cls.engine = create_engine(
            f'mysql+pymysql://{cls.user}:{cls.password}@{cls.host}:{cls.port}',
            pool_pre_ping=True
        )
        cls.engine.execute(f'CREATE DATABASE IF NOT EXISTS {cls.dbname}')
        cls.engine.execute('USE {cls.dbname}')
        # for table in listdir('table_schemas'):
        #     with open(f'./table_schemas/{table}') as schema:
        #         c.execute(schema.read())
        # cls.connection.commit()
        cls.engine.execute('select 1')

    @classmethod
    def insert_into_table(cls, table, record):
        e = cls.get_engine()
        e.execute(
            f'''INSERT INTO {table} ({tuple(record.keys())}) VALUES ({tuple(record.values())})'''
        )
        e.commit()

    @classmethod
    def update_table(cls, table, id_key, id_value, update_key, update_value):
        e = cls.get_engine()
        e.execute(
            f'''UPDATE {table} SET {update_key} = {update_value} WHERE {id_key} = {id_value}'''
        )
        e.commit()
