from flask import Blueprint, jsonify

face_attendance_bp = Blueprint('face-attendance', __name__, url_prefix='/face-attendance')

@face_attendance_bp.route('/health', methods=['GET'])
def health_check():
    """
    Simple health check endpoint to verify if the app is up and running.
    Returns:
        JSON response with the status of the app.
    """
    try:
        response = {
            "status": "ok",
            "message": "Service is healthy. API is running normally",
        }
        return jsonify(response), 200

    except Exception as e:
        response = {
            "status": "error",
            "message": f"API isn't running. Health check failed: {str(e)}"
        }
        return jsonify(response), 500