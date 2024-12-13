--- Facenet 512
INSERT INTO identities_fn512 (img_name, embedding)
VALUES (%s, %s);

--- Dlib
INSERT INTO identities_dlib (img_name, embedding) 
VALUES (%s, %s);
