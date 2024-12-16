import os
import time
import logging
from psycopg2 import pool
from dotenv import load_dotenv

load_dotenv()
db_name = os.getenv('DB_NAME', 'default_db_name')
db_user = os.getenv('DB_USER', 'default_user')
db_pass = os.getenv('DB_PASS', 'default_password')
db_host = os.getenv('DB_HOST', 'localhost')
db_port = os.getenv('DB_PORT', '5432')

dsn = f"dbname='{db_name}' user='{db_user}' password='{db_pass}' host='{db_host}' port={db_port}"
db_pool = pool.SimpleConnectionPool(minconn=1, maxconn=10, dsn=dsn)

def get_local_db(db_pool=db_pool):
    logging.debug("Getting database connection.")
    conn = db_pool.getconn()
    cursor = conn.cursor()

    return conn, cursor

def retun_to_pool(conn, db_pool=db_pool):
    db_pool.putconn(conn)

def count_time(start_time, db=None):
    """Calculate the time used for process"""

    if db:
        return round((time.time() - start_time)* 1000)
    else:
        return round((time.time() - start_time), 2)