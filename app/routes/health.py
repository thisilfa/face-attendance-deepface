from flask import Blueprint, jsonify

health_bp = Blueprint('api-health', __name__)

@health_bp.route('/start', methods=['GET'])
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