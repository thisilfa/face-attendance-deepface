import os
import time
from datetime import datetime
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename

def handle_unprocessed(image_file):
    save_img('unprocessed', image_file, None)
    return {
        'message': "Internal error while processing this image.",
        'data': {
            'registration_number': None,
            'name': None
        }
    }

def handle_no_face_detected(image_file):
    save_img('not-detected', image_file, None)
    return {
        'message': "Face not detected in the image.",
        'data': {
            'registration_number': None,
            'name': None
        }
    }

def handle_spoofing_img(image_file):
    save_img('spoofing', image_file, None)
    return {
        'message': "Spoofing detected.",
        'data': {
            'registration_number': None,
            'name': None
        }
    }


def handle_no_face_recognized(image_file):
    save_img('unrecognized', image_file, None)
    return {
        'message': "Data not found in the database",
        'data': {
            'registration_number': None,
            'name': None
        }
    }


def handle_mismatch_face_data(image_file):
    save_img('mismatched', image_file, None)
    return {
        'message': "Found a mismatch data with this image.",
        'data': {
            'registration_number': None,
            'name': None
        }
    }


def handle_face_recognized(image_file, no_ind, name):
    save_img('recognized', image_file, name)
    return {
        'message': "Successfully recognized.",
        'data': {
            'registration_number': no_ind,
            'name': name
        }
    }


def save_img(metrics, image_file, name):
    dir_map = {
        'not-detected': 'not-detected',
        'spoofing': 'spoofing',
        'unrecognized': 'unrecognized',
        'mismatched': 'mismatched',
        'recognized': 'recognized',
        'unprocessed': 'unprocessed'
    }
    base_path = dirname(realpath('__file__'))
    dataset_path = datetime.now().strftime('%Y-%m-%d')
    folder_path = join(base_path, 'public', 'images', dataset_path, dir_map[metrics])

    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)

    extension = secure_filename(image_file.filename).split('.')[1]
    filename = f"{folder_path}/{int(time.time())}_{name if name else ''}.{extension}"

    image_file.seek(0)
    image_file.save(filename)