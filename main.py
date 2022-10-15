import uvicorn
from typing import List
from fastapi import Depends, FastAPI, HTTPException


from api.model import crud, models, schemas
from api.model.database import SessionLocal, engine
from api.routes import importarDados, rotaAlgoritmoGenetico, rotaAlimentos, rotaPratos


app = FastAPI(
    title="INutriEscolar API",
    description="API INutriEscolar",
    version='1.0.0'
)


models.Base.metadata.create_all(bind=engine)


@app.get("/")
def index():
    return {"Bem Vindo ao INutriEscolar"}


app.include_router(rotaAlimentos.alimento, tags=['Alimento'])
app.include_router(rotaPratos.prato, tags=['Prato'])
app.include_router(rotaAlgoritmoGenetico.algoritmo, tags=['Algoritmo genético'])
app.include_router(importarDados.data, tags=['Data'])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)