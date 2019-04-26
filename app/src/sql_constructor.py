from pypika import MySQLQuery as Query, Table

class Constructor:
    def __init__(self, db_name):
        self.dbname = db_name

    def create_database(self):
        return f'CREATE DATABASE IF NOT EXISTS {self.dbname}'

    def use_database(self):
        return f'USE {self.dbname}'

    def insert_record(self, table, record):
        table = Table(table)
        columns = tuple(record.keys())
        values = tuple(record.values())
        q = Query.into(table).columns(*columns).insert(values)
        return q.get_sql()

    def bulk_insert(self, table, records):
        table = Table(table)
        columns = tuple(records[0].keys())
        values = tuple(
            tuple(record.values())
            for record in records
        )
        q = Query.into(table).columns(*columns).insert(*values)
        return q.get_sql()

    def update_record(self, table, record, **where_values):
        table = Table(table)
        q = Query.update(table)
        for k, v in record.items():
            q = q.set(getattr(table, k), v)
        for k, v in where_values.items():
            q = q.where(getattr(table, k) == v)
        return q.get_sql()

    def select(self, table, fields, **where_values):
        table = Table(table)
        q = Query.from_(table)
        for field in fields:
            q = q.select(getattr(table, field))
        for k, v in where_values.items():
            q = q.where(getattr(table, k) == v)
        return q.get_sql()
