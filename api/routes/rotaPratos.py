from fastapi import FastAPI, APIRouter, Depends
from api.model import crud, models, schemas
from sqlalchemy.orm import Session
from typing import List

from api.model.database import SessionLocal, engine

prato = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@prato.post("/prato/criar/")
def novoPrato( prato: schemas.Prato, db: Session = Depends(get_db)):
    prato = crud.criarPrato(db=db, prato=prato)
    return prato


@prato.get("/prato/buscar/", response_model=List[schemas.Prato])
def retornaTodosPratos(db: Session = Depends(get_db)):
    pratos = crud.buscarTodosPratos(db)
    return pratos


@prato.get("/prato/buscar/{prato_id}")
def retornaPratoPorId(prato_id: int, db: Session = Depends(get_db)):
    prato = crud.buscarPratoPorId(db, prato_id)
    return prato


@prato.post("/prato/adicionar/alimento/")
def adicionarAlimentoPrato(criacao: schemas.Criacao, db: Session = Depends(get_db)):
    return crud.criarCriacao(db=db, criacao=criacao)


@prato.post("/prato/adicionar/alimentos/")
def adicionarAlimentoPrato(criacao: schemas.CriacaoList, db: Session = Depends(get_db)):
    return crud.criarCriacaoList(db=db, criacao=criacao)


@prato.delete("/prato/deletar/{prato_id}")
def excluirPrato(prato_id: int, db: Session = Depends(get_db)):
    if crud.deletarPrato(db, prato_id):
        return {"message": f'O prato {prato_id} foi deletado!'}
    else:
        return {"message": f'O prato {prato_id} não foi encontrado!'}
