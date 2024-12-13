--- Facenet 512
DELETE FROM identities_fn512 
WHERE id = %s;

--- Dlib
DELETE FROM identities_dlib 
WHERE id = %s;