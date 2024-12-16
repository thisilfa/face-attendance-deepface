import os
import logging

from flask import Blueprint, request, jsonify
from os.path import dirname, join, realpath

from app.utils.general import  get_local_db, retun_to_pool

deleter_bp = Blueprint('deleter', __name__)

base_path = dirname(realpath(__file__))
data_path = join(base_path, 'public', 'registered_images')

@deleter_bp.route('/<string:no_ind>', methods=["DELETE"])
def delete_face(no_ind):
    # Get parameters from the request
    no_ind = no_ind.upper()
    id_photo = request.form.get("id")
    
    if not no_ind or not id_photo:
        logging.error(f"Missing parameters: no_ind={no_ind}, face_id={id_photo}")
        return jsonify({'status': 'error', 'message': 'Missing no_ind or id'}), 400
    
    try:
        logging.info(f"Deleting face with id {id_photo} and no_ind {no_ind}")
        conn, cursor = get_local_db()

        cursor.execute("SELECT id, img_name FROM identities_fn512 img_name like %s", (f'%{no_ind}%',))
        list_data_facenet = cursor.fetchall()

        if not list_data_facenet:
            logging.warning(f"No record found for id {id_photo} and no_ind {no_ind}")
            return jsonify({'status': 'error', 'message': 'No record found with the given id and no_ind'}), 404

        img_name = list_data_facenet[1]
        img_filepath = f"{join(data_path, img_name)}.jpg"

        if os.path.exists(img_filepath):
            os.remove(img_filepath)
            logging.info(f"Deleted file {img_filepath}")
        else:
            logging.error(f"Image file not found on the server: {img_filepath}")
            return jsonify({'status': 'error', 'message': 'Image file not found on the server'}), 404

        cursor.execute("DELETE FROM identities_fn512 WHERE id = %s", (list_data_facenet[0],))
        cursor.execute("DELETE FROM identities_dlib WHERE id = %s", (list_data_facenet[0],))

        conn.commit()
        logging.info(f"Deleted face data with id {id_photo} and no_ind {no_ind}")
        return jsonify({
            'status': 'success',
            'message': f'Deleted face data with id {id_photo} and no_ind {no_ind}',
            'file_deleted': True
        }), 200

    except Exception as e:
        logging.exception(f"Error deleting face with id {id_photo} and no_ind {no_ind}")
        conn.rollback()
        return jsonify({"status": "error", "message": "An internal error was occured when updating the data."}), 500
    
    finally:
        cursor.close()
        retun_to_pool(conn)