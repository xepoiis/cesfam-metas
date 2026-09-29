from fastapi import FastAPI
from database import engine, Base
import models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API CESFAM Santa Rosa",
    description="Motor de cálculo IAAPS y Metas Sanitarias"
)

@app.get("/")
def estado_servidor():
    return {"estado": "En línea", "mensaje": "¡Motor de Cálculo CESFAM y Base de Datos operativos!"}