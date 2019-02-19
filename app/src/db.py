from dotenv import load_dotenv
from sqlalchemy import create_engine
from os import listdir, getenv
from datetime import datetime as dt
from src.sql_constructor import Constructor

load_dotenv()


class Database:
    user = getenv('DB_USER')
    password = getenv('DB_PASSWORD')
    host = getenv('DB_HOST')
    port = getenv('DB_PORT')
    dbname = getenv('DB_NAME')
    conn_str = f'mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}'

    engine = None
    qb = Constructor(dbname)

    @classmethod
    def get_engine(cls):
        if not cls.engine:
            cls.engine = create_engine(cls.conn_str, pool_pre_ping=True)
        return cls.engine

    @classmethod
    def initialize(cls):
        cls.execute_query(cls.qb.create_database())
        cls.execute_query(cls.qb.use_database())
        for table in listdir('table_schemas'):
            with open(f'./table_schemas/{table}') as schema:
                cls.execute_query(schema.read())

    @classmethod
    def update_history(cls, table_name, file_name):
        record = {'name': file_name, 'inserted_date': dt.now().date()}
        cls.execute_query(cls.qb.insert_record(table_name, record))

    @classmethod
    def check_history(cls, table_name, file_name):
        rslt = cls.execute_query(cls.qb.select(table_name, 'name', name=file_name))
        if rslt: return True
        return False

    @classmethod
    def execute_query(cls, query):
        e = cls.get_engine()
        return e.execute(query)
