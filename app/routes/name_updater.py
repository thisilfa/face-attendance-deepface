import os
import logging

from flask import Blueprint, request, jsonify
from os.path import dirname, join, realpath

from app.utils.general import  get_local_db, retun_to_pool

name_updater_bp = Blueprint('update-name', __name__)

base_path = dirname(realpath(__file__))
data_path = join(base_path, 'public', 'registered_images')

@name_updater_bp.route('/<string:no_ind>', methods=["PUT"])
def update_name(no_ind):
    # Get parameters from the request
    no_ind = no_ind.upper()
    new_name = request.form.get("new_name").upper()
    
    if not no_ind or not new_name:
        logging.error(f"Missing parameters: no_ind={no_ind}, new_name={new_name}")
        return jsonify({'status': 'error', 'message': 'Missing no_ind or new_name'}), 400
    
    try:
        logging.info(f"Updating name for no_ind {no_ind} to {new_name}")
        conn, cursor = get_local_db()

        cursor.execute("SELECT id, img_name FROM identities_fn512 img_name like %s", (f'%{no_ind}%',))
        list_data_facenet = cursor.fetchall()

        if not list_data_facenet:
            logging.warning(f"No record found for no_ind {no_ind}")
            return jsonify({'status': 'error', 'message': 'No record found with the given no_ind'}), 404

        for data in list_data_facenet:
            old_img_name = data[1]
            id_photo = old_img_name.split('_')[0]
            
            new_img_name = '_'.join(id_photo, no_ind, new_name)

            old_filepath = f"{join(data_path, old_img_name)}.jpg"
            new_filepath = f"{join(data_path, new_img_name)}.jpg"

            if os.path.exists(old_filepath):
                os.rename(old_filepath, new_filepath)
                logging.info(f"Renamed file from {old_filepath} to {new_filepath}")
            else:
                logging.error(f"Image file not found on the server: {old_filepath}")
                return jsonify({'status': 'error', 'message': 'Image file not found on the server'}), 404

            cursor.execute(
                "UPDATE identities_fn512 SET img_name = %s WHERE id = %s",
                (new_img_name, data[0])
            )
            cursor.execute(
                "UPDATE identities_dlib SET img_name = %s WHERE img_name = %s",
                (new_img_name, old_img_name)
            )

        conn.commit()
        logging.info(f"Updated name for {len(data)} records")
        return jsonify({'status': 'success', 'message': f'Updated name for {len(data)} records'}), 200

    except Exception as e:
        logging.exception(f"Error updating noame with employee id: {no_ind}")
        conn.rollback()
        return jsonify({"status": "error", "message": "An internal error was occured when updating the data."}), 500
    
    finally:
        cursor.close()
        retun_to_pool(conn)
