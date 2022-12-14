from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from api.model import crud, models, schemas
from api.model.database import SessionLocal, engine


alimento = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@alimento.post("/alimento/criar/")
def novoAlimento(alimento: schemas.Alimento, db: Session = Depends(get_db)):
    alimento = crud.criarAlimento(db=db, alimento=alimento)
    return alimento

@alimento.get("/alimento/listar/")
def novoAlimento(db: Session = Depends(get_db)):
    alimento = crud.buscarTodosAlimentos(db=db)
    return alimento

@alimento.get("/alimento/buscar/", response_model=List[schemas.Alimento])
def retornaTodosAlimentos(db: Session = Depends(get_db)):
    alimentos = crud.buscarTodosAlimentos(db)
    return alimentos


@alimento.get("/alimento/buscar/{alimento_id}")
def retornaAlimentoPorId(alimento_id: int, db: Session = Depends(get_db)):
    alimento = crud.buscarAlimentoPorId(db, alimento_id)
    return alimento


@alimento.delete("/alimento/deletar/{alimento_id}")
def excluirAlimento(alimento_id: int, db: Session = Depends(get_db)):
    if crud.deletarAlimento(db, alimento_id):
        return {"message": f'O alimento {alimento_id} foi deletado!'}
    else:
        return {"message": f'O alimento {alimento_id} não foi encontrado!'}