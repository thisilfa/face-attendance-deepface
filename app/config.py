import os
from psycopg2 import pool
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

SERVER_DB_URI = os.getenv("SERVER_DB_URI")

server_engine = create_engine(SERVER_DB_URI)
ServerSession = sessionmaker(bind=server_engine)

Base = declarative_base()
