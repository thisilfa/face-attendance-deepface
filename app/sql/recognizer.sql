SELECT id, img_name, embedding<->:embedding AS distance_fn512
FROM identities_fn512
WHERE embedding<->:embedding::vector<:threshold
ORDER BY distance_fn512 ASC
LIMIT 1;

--- Dlib
SELECT id, img_name, embedding<->:embedding AS distance_dlib
FROM identities_dlib
WHERE embedding<->:embedding<:threshold
ORDER BY distance_dlib ASC
LIMIT 1