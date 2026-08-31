from fastapi import FastAPI

from app.routes.classe_route import router as classe_router
from app.routes.etudiant_route import router as etudiant_router
from app.routes.examen_route import router as examen_router
from app.routes.participation_route import router as affectation_router
from app.routes.presence_route import router as presence_router
from app.routes.etudiant_route import router as etudiant_router

app = FastAPI()


app.include_router(classe_router)
app.include_router(etudiant_router)
app.include_router(examen_router)
app.include_router(affectation_router)
app.include_router(presence_router)
app.include_router(etudiant_router)
