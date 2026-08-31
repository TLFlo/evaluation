from pathlib import Path

import cv2
import numpy as np
from insightface.app import FaceAnalysis


face_app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])

face_app.prepare(ctx_id=0, det_size=(640, 640))


def create_embedding(photo_path: str, embedding_path: str) -> None:
    # 1. Vérifier que la photo existe
    if not Path(photo_path).exists():
        raise ValueError("La photo n'existe pas.")

    # 2. Charger l'image
    image = cv2.imread(photo_path)

    if image is None:
        raise ValueError("Impossible de lire la photo.")

    # 3. Détecter les visages
    faces = face_app.get(image)

    # 4. Vérifier le nombre de visages
    if len(faces) == 0:
        raise ValueError("Aucun visage détecté sur la photo.")

    if len(faces) > 1:
        raise ValueError(
            "Plusieurs visages détectés. La photo doit contenir un seul visage."
        )

    # 5. Récupérer le visage
    face = faces[0]

    # 6. Récupérer l'embedding
    embedding = face.embedding

    if embedding is None:
        raise ValueError("Impossible de générer l'embedding.")

    # 7. Créer le dossier
    embedding_file = Path(embedding_path)

    embedding_file.parent.mkdir(parents=True, exist_ok=True)

    # 8. Sauvegarder
    np.save(embedding_file, embedding)


def verifier_visage(photo_path: str, embedding_path: str, seuil: float = 0.5) -> bool:
    if not Path(photo_path).exists():
        raise ValueError("La photo n'existe pas.")

    if not Path(embedding_path).exists():
        raise ValueError("L'embedding n'existe pas.")

    # Charger la photo
    image = cv2.imread(photo_path)

    if image is None:
        raise ValueError("Impossible de lire la photo.")

    # Détecter le visage
    faces = face_app.get(image)

    if len(faces) == 0:
        raise ValueError("Aucun visage détecté.")

    if len(faces) > 1:
        raise ValueError("Plusieurs visages détectés.")

    # Embedding de la nouvelle photo
    new_embedding = faces[0].embedding

    # Embedding enregistré
    stored_embedding = np.load(embedding_path)

    # Normalisation
    new_embedding = new_embedding / np.linalg.norm(new_embedding)

    stored_embedding = stored_embedding / np.linalg.norm(stored_embedding)

    # Similarité cosinus
    similarity = np.dot(new_embedding, stored_embedding)

    print(f"Similarité : {similarity:.4f}")

    return similarity >= seuil
