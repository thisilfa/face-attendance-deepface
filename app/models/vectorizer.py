from sqlalchemy.types import UserDefinedType
from sqlalchemy import Integer
import psycopg2
import psycopg2.extras

class PGVector(UserDefinedType):
    def __init__(self, dimension: int):
        self.dimension = dimension
        super().__init__()

    def bind_expression(self, bindvalue):
        return bindvalue

    def column_expression(self, col):
        return col

    def process_bind_param(self, value, dialect):
        if isinstance(value, list): 
            return psycopg2.Binary(bytearray(value)) 
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return list(value)
        return value

    def result_processor(self, dialect, column_type):
        return self.process_result_value
