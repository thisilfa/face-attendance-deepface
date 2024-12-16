import os
import re
import cv2
import logging
import numpy as np

from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from os.path import dirname, join, realpath

from app.utils.deepface_util import load_embedding
from app.utils.general import  get_local_db, retun_to_pool

register_bp = Blueprint('registration', __name__)

@register_bp.route('/start', methods=["POST"])
def register_face():
    logging.info("Register face endpoint called.")
    raw_noind = request.form.get("no_ind")
    if 'image' not in request.files or not raw_noind:
        logging.warning("No file part or missing no_ind.")
        return jsonify({'status': 'error', 'message': 'No file part or missing no_ind'}), 400
    
    image_file = request.files['image']
    img = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)

    try:
        facenet_objs = load_embedding('facenet_512', img)
        dlib_objs = load_embedding('dlib', img)

        conn, cursor = get_local_db()
        
        cursor.execute("SELECT img_name FROM identities_fn512 WHERE img_name like %s", (f'%{raw_noind}%',))
        list_data_facenet = cursor.fetchall()
        print(list_data_facenet)

        id_photo = find_id_photo(list_data_facenet)
        user, no_id = extract_user_detail(raw_noind)
        
        user_data = f"{str(id_photo)}_{user}"

        cursor.execute(
            "INSERT INTO identities_fn512 (img_name, embedding) VALUES (%s, %s)",
            (user_data, facenet_objs)
        )
        cursor.execute(
            "INSERT INTO identities_dlib (img_name, embedding) VALUES (%s, %s)",
            (user_data, dlib_objs)
        )
        
        conn.commit()
        save_img(image_file, user_data)
        logging.info(f"Face registered for identity: {user_data}")
        return jsonify({"status": "success", "message": f"Face registered for identity: {user_data}"}), 200

    except Exception as e:
        logging.error(f"Error during registration: {e}", exc_info=True)
        conn.rollback()
        return jsonify({"status": "error", "message": "An internal error was occured during registration"}), 500
    
    finally:
        cursor.close()
        retun_to_pool(conn)

def find_id_photo(list_data):
    if list_data==[]:
        return 1

    list_id_photos = [int(re.search(r'(\d+)_', item[0]).group(1)) for item in list_data]
    sorted_ids = sorted(list_id_photos)
    max_id = sorted_ids[-1]

    for i in range(1, max_id):
        if i not in sorted_ids:
            return i
    
    return max_id + 1

def extract_user_detail(raw_noind):
    user = os.path.splitext(raw_noind)[0].upper()
    no_id = re.findall(r'^[A-Za-z0-9]+', user)[0]
    
    return user, no_id

def save_img(image_file, user_data):
    base_path = dirname(realpath('__file__'))
    folder_path = join(base_path, 'public', 'registered-images')

    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)

    extension = secure_filename(image_file.filename).split('.')[1]
    filename = f"{folder_path}/{user_data}.{extension}"

    image_file.seek(0)
    image_file.save(filename)