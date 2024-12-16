# utils.py

import io
import logging
import pandas as pd
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from app.config import ServerSession 
from app.models.serverai_analytic import  AnalyticsFaceAttendanceLocalServices

def append_data(**kwargs):
    try:
        columns = kwargs.keys()
        data = [list(kwargs.values())]
        df = pd.DataFrame(data, columns=columns)

        df['request_date'] = pd.to_datetime(df['request_date'], format='%Y-%m-%d %H:%M:%S')

        session = ServerSession()

        for idx, row in df.iterrows():
            analytics = AnalyticsFaceAttendanceLocalServices(
                id_api=row['id_api'],
                ip_address=row['ip_address'],
                request_date=row['request_date'],
                url_api=row['url_api'],
                response=row['response'],
                response_time=row['response_time']
            )
            session.add(analytics)

        session.commit()

        logging.info(f"Successfully appended {len(df)} records to the analytics table.")
    except SQLAlchemyError as e:
        session.rollback()
        logging.error(f"Error appending data: {e}")
    finally:
        session.close()

