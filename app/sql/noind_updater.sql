--- Facenet 512
UPDATE identities_fn512 
SET img_name = %s 
WHERE id = %s;

--- Dlib
UPDATE identities_dlib 
SET img_name = %s 
WHERE img_name = %s;