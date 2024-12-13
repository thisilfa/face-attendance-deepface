# app/__init__.py
from flask import Flask
from app.routes.recognizer import face_attendance_bp 
def create_app():
    app = Flask(__name__)

    app.register_blueprint(face_attendance_bp) 

    return app
