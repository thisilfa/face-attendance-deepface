import os
from psycopg2 import pool
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

LOCAL_DB_URI = os.getenv("LOCAL_DB_URI")
SERVER_DB_URI = os.getenv("SERVER_DB_URI")

# local_pool = pool.SimpleConnectionPool(minconn=1, maxconn=10, dsn=LOCAL_DB_URI)

local_engine = create_engine(LOCAL_DB_URI)
LocalSession = sessionmaker(bind=local_engine)

server_engine = create_engine(SERVER_DB_URI)
ServerSession = sessionmaker(bind=server_engine)

Base = declarative_base()
