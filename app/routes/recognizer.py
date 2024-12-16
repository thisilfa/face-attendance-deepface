import os
import cv2
import time
import logging
import numpy as np

from flask import Blueprint, request, jsonify

from app.utils.deepface_util import load_embedding
from app.utils.general import count_time, get_local_db, retun_to_pool
from app.services.response_handler import handle_face_recognized, handle_mismatch_face_data, handle_no_face_detected, handle_no_face_recognized, handle_spoofing_img, handle_unprocessed

recognizer_bp = Blueprint('prediction', __name__)

@recognizer_bp.route('/start', methods=['POST'])
def predict():
    if 'image' not in request.files:
        logging.warning("No file part in request.")
        return jsonify({'status': 'error', 'message': 'No file part'}), 400
    
    image_file = request.files['image']
    if image_file.filename == '':
        logging.warning("No selected file.")
        return jsonify({'status': 'error', 'message': 'No selected file'}), 400
    
    img = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
    response, http_code = image_preprocess(img, image_file)
    return jsonify(response), http_code


def image_preprocess(img, image_file, facenet_thres=0.31, dlib_thres=0.4):
    try:
        conn, cursor = get_local_db()

        start_time = time.time()

        facenet_objs = load_embedding('facenet_512', img)
        dlib_objs = load_embedding('dlib', img)

        if facenet_objs==[]:
            response = handle_no_face_detected(image_file)
            response['time'] = count_time(start_time)

            return response, 200

        cursor.execute(
            """
            SELECT id, img_name, embedding <=> %s AS distance_fn512
            FROM identities_fn512
            WHERE embedding <=> %s < %s
            ORDER BY distance_fn512 ASC
            LIMIT 1
            """,
            (str(facenet_objs), str(facenet_objs), facenet_thres)
        )
        raw_fn_result = cursor.fetchone()

        if raw_fn_result:
            facenet_result = raw_fn_result
        else:
            facenet_result = None

        cursor.execute(
            """
            SELECT id, img_name, embedding <-> %s AS distance_dlib
            FROM identities_dlib
            WHERE embedding <-> %s < %s
            ORDER BY distance_dlib ASC
            LIMIT 1
            """,
            (str(dlib_objs), str(dlib_objs), dlib_thres)
        )
        raw_dlib_result = cursor.fetchone()

        if raw_dlib_result:
            dlib_result = raw_dlib_result
        else:
            dlib_result = None

        response, code = result_post_process(facenet_result, dlib_result, image_file, start_time)

    except Exception as e:
        logging.error(f"Error during image processing: {e}", exc_info=True)
        conn.rollback()

        response = handle_unprocessed(image_file)

        return response, 500
    
    finally:
        cursor.close()
        retun_to_pool(conn)

    return response, code


def result_post_process(facenet_result, dlib_result, image_file, start_time):

    if facenet_result and dlib_result:
        name = facenet_result[1].split('/')[-1].split('_')[-1].split('.')[0]
        facenet_id = os.path.splitext(os.path.basename(facenet_result[1]))[0].split('_')[1]
        dlib_id = os.path.splitext(os.path.basename(dlib_result[1]))[0].split('_')[1]

        if facenet_id == dlib_id:
            result = handle_face_recognized(image_file, facenet_id, name)
            result['time'] = count_time(start_time)

            logging.info(f"Face detected successfully facenet512:\n{facenet_result} and dlib results:\n{dlib_result}.")
        
            return result, 200
        else:
            result = handle_mismatch_face_data(image_file)
            result['time'] = count_time(start_time)

            logging.warning(f"Face not found: Mismatch between facenet512:\n{facenet_result} and dlib results:\n{dlib_result}.")
            
            return result, 200
    else:
        result = handle_no_face_recognized(image_file)
        result['time'] = count_time(start_time)

        logging.warning(f"Face not found in the database facenet512:\n{facenet_result} and dlib results:\n{dlib_result}.")
        
        return result, 200
    