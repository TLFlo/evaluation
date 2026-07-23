from app.core.database import engine

try:
    with engine.connect() as connection:
        print("Connexion réussie !")
except Exception as e:
    print(e)
