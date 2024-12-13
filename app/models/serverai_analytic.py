# app/models/analytics.py
import os
from app.config import Base
from sqlalchemy import Column, Integer, String, DateTime

DB_SCHEMA = os.getenv('DB_SCHEMA', 'public') 
ANALYTICS_TABLE_NAME = os.getenv('ANALYTICS_TABLE_NAME', 'default_analytics_table')
SERVICES_TABLE_NAME = os.getenv('SERVICES_TABLE_NAME', 'default_face_attendance_table')

class AnalyticsFaceAttendanceLocalServices(Base):
    __tablename__ = ANALYTICS_TABLE_NAME
    __table_args__ = {'schema': DB_SCHEMA}

    id_api = Column(Integer, nullable=False)
    id_request = Column(Integer, primary_key=True)
    ip_address = Column(String(20), nullable=False)
    request_date = Column(DateTime, nullable=False)
    url_api = Column(String(100), nullable=False)
    response = Column(String(255), nullable=False)
    response_time = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<AnalyticsFaceAttendanceLocalServices(id_request={self.id_request}, request_date={self.request_date}, response_time={self.response_time})>"

class FaceAttendanceLocalServices(Base):
    __tablename__ = SERVICES_TABLE_NAME
    __table_args__ = {'schema': DB_SCHEMA}

    id_api = Column(Integer, primary_key=True)
    service_name = Column(String(50), nullable=False)
    service_host = Column(String(20), nullable=False)
    port = Column(Integer, nullable=False)
    base_url = Column(String(50), nullable=False)
    status = Column(String, nullable=True)

    def __repr__(self):
        return f"<FaceAttendanceLocalServices(id_api={self.id_api}, service_name={self.service_name})>"
