import os
import cv2
import time
import numpy as np

from sqlalchemy import text
from flask import request, jsonify

from app.config import LocalSession
from app.utils.deepface_util import load_embedding
from app.utils.general import load_sql_query, count_time
from app.services.response_handler import handle_face_recognized, handle_mismatch_face_data, handle_no_face_detected, handle_no_face_recognized, handle_spoofing_img

from .health import face_attendance_bp

@face_attendance_bp.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        # logging.warning("No file part in request.")
        return jsonify({'status': 'error', 'message': 'No file part'}), 400
    
    image_file = request.files['image']
    if image_file.filename == '':
        # logging.warning("No selected file.")
        return jsonify({'status': 'error', 'message': 'No selected file'}), 400
    
    img = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
    result, http_code = image_preprocess(img, image_file)
    return jsonify(result), http_code


def image_preprocess(img, image_file, facenet_thres=0.31, dlib_thres=0.4):
    try:
        session = get_db_session()

        start_time = time.time()

        facenet_objs = load_embedding('facenet_512', img)
        dlib_objs = load_embedding('dlib', img)

        if facenet_objs==[]:
            result = handle_no_face_detected(image_file)
            result['time'] = count_time(start_time)

            return result, 200

        queries = load_sql_query('recognizer.sql')
        facenet_query = queries.split("--- Dlib")[0].strip()
        dlib_query = queries.split("--- Dlib")[1].strip()

        result = session.execute(text(facenet_query), {'embedding': facenet_objs, 'threshold': facenet_thres}).fetchone()
        if result:
            facenet_result = result
        else:
            facenet_result = None

        result = session.execute(text(dlib_query), {'embedding': dlib_objs, 'threshold': dlib_thres}).fetchone()
        if result:
            dlib_result = result
        else:
            dlib_result = None

        response, code = result_post_process(facenet_result, dlib_result, image_file, start_time)

    except Exception as e:
        # Handle exceptions and ensure the session is closed in case of errors
        session.rollback()  # Rollback any transactions if something goes wrong
        raise e

    finally:
        # Always close the session when done
        session.close()

    return response, code


def result_post_process(facenet_result, dlib_result, image_file, start_time):

    if facenet_result and dlib_result:
        name = facenet_result[1].split('/')[-1].split('_')[-1].split('.')[0]
        facenet_id = os.path.splitext(os.path.basename(facenet_result[1]))[0].split('_')[1]
        dlib_id = os.path.splitext(os.path.basename(dlib_result[1]))[0].split('_')[1]

        if facenet_id == dlib_id:
            # Save image to success directory
            result = handle_face_recognized(image_file, facenet_id, name)
            result['time'] = count_time(start_time)

            # logging.info(f"Face detected successfully facenet512:\n{fn512_result} and dlib results:\n{dlib_result}. \nImage saved to {success_path}")
        
            return result, 200
        else:
            # Save image to fail directory
            result = handle_mismatch_face_data(image_file)
            result['time'] = count_time(start_time)

            # logging.warning(f"Face not found: Mismatch between facenet512:\n{fn512_result} and dlib results:\n{dlib_result}. \nImage saved to {fail_path}")
            
            return result, 200
    else:
        # Save image to fail directory
        result = handle_no_face_recognized(image_file)
        result['time'] = count_time(start_time)

        # logging.warning(f"Face not found in the database facenet512:\n{fn512_result} and dlib results:\n{dlib_result}. \nImage saved to {fail_path}")
        
        return result, 200
    
def get_db_session():
    """Retrieve an SQLAlchemy session using the sessionmaker."""
    session = LocalSession()  # Get a session from the session factory
    return session