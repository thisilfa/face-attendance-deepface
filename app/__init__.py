import json
import logging
import time
from datetime import datetime
from flask import Flask, request
from werkzeug.exceptions import HTTPException
from app.routes import register_routes
from app.utils.general import count_time
from app.services.serverai_analytic_service import append_data
from app.logger import start_background_tasks

def create_app():
    app = Flask(__name__)

    start_background_tasks()

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """
        Handle exceptions and return JSON response.
        """
        response = e.get_response()
        response.data = json.dumps({"message": e.description})
        response.content_type = "application/json"

        logging.error(f"status: {e.code} request: {request.remote_addr} "
                      f"{request.method} {request.url} response: {response.data}")
        return response, e.code

    @app.after_request
    def append_analytics(response):
        start_time = time.time()
        code = response.status_code

        try:
            result = response.get_json() if response.is_json else {}
            result_data = json.dumps(result)

            ip_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)

            append_data(id_api=1,  
                        ip_address=ip_addr,
                        request_date=datetime.now(),
                        url_api=request.url,
                        response=result_data,
                        response_time=result['time'] *1000)
            print(json.dumps(result))

            logging.info(f"Connection successful, result data has been appended to PostgreSQL")

        except Exception as e:
            logging.error(f"Connection failed to PostgreSQL", exc_info=True)

        return response

    register_routes(app)

    return app
