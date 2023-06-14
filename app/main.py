from fastapi import FastAPI
from . import models
from .database import engine
from .routers import user, categorie, clientele, marque, produit, taille, unite_de_mesure, auth
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["https://boutiquehanen.onrender.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(categorie.router)
app.include_router(clientele.router)
app.include_router(marque.router)
app.include_router(taille.router)
app.include_router(unite_de_mesure.router)
app.include_router(produit.router)

@app.get("/")
async def root():
  return {"message": "Welcome ! This is Hanen's API"}
