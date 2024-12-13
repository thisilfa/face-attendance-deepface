from deepface import DeepFace

def load_embedding(model, img):
    if model=='facenet_512':
        obj = DeepFace.represent(
                        img_path=img, 
                        model_name="Facenet512",
                        enforce_detection=False,
                        detector_backend="opencv",
                        align=False, #default True
                        expand_percentage=0,
                        normalization="base",
                        anti_spoofing=False,
                        max_faces=None
                        )
        return obj[0]["embedding"]
    elif model=='dlib':
        obj = DeepFace.represent(
                        img_path=img, 
                        model_name="Dlib",
                        enforce_detection=False,
                        detector_backend="opencv",
                        align=False, #default True
                        expand_percentage=0,
                        normalization="base",
                        anti_spoofing=False,
                        max_faces=None
                        )
        return obj[0]["embedding"]
    else:
        return None
    
