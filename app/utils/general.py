import os
import time
from os.path import dirname, join, abspath

def load_sql_query(file_path):
    """Load and return the SQL query from a `.sql` file."""

    base_path = join('/', *dirname(abspath(__file__)).split(os.sep)[:-1])
    sql_dir = join(base_path, 'sql')
    sql_path = join(sql_dir, file_path)
    
    with open(sql_path, 'r') as file:
        return file.read()


def count_time(start_time, db=None):
    """Calculate the time used for process"""

    if db:
        return round((time.time() - start_time)* 1000)
    else:
        return round((time.time() - start_time), 2)