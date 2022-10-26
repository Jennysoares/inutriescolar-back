from sqlalchemy.orm import Session

from . import models, schemas


def buscarTodosAlimentos(db: Session):
    return db.query(models.Alimento).all()


def buscarAlimentoPorId(db: Session, alimento_id: int):
    alimento = db.query(models.Alimento).filter(models.Alimento.id == alimento_id).first()
    return alimento


def buscarTodosPratos(db: Session):
    return db.query(models.Prato).all()


def buscarPratoPorId(db: Session, prato_id: int):
    prato = db.query(models.Prato).filter(models.Prato.id == prato_id).first()
    return prato


def criarAlimento(db: Session, alimento: schemas.Alimento):
    db_alimento = models.Alimento(**alimento.dict())
    db.add(db_alimento)
    db.commit()
    db.refresh(db_alimento)
    return db_alimento


def criarPrato(db: Session, prato: schemas.Prato):
    db_prato = models.Prato(**prato.dict())
    db.add(db_prato)
    db.commit()
    db.refresh(db_prato)
    return db_prato


def criarCriacao(db: Session, criacao: schemas.Criacao):
    db_criacao = models.Criacao(**criacao.dict())
    db.add(db_criacao)
    db.commit()
    db.refresh(db_criacao)
    return db_criacao

def criarCriacaoList(db: Session, criacao: schemas.CriacaoList):
    for item in criacao.data:
        db_criacao = models.Criacao(**item.dict())
        db.add(db_criacao)
        db.commit()
        db.refresh(db_criacao)
    return db_criacao

def deletarAlimento(db: Session, alimento_id):
    alimento = buscarAlimentoPorId(db, alimento_id)
    if alimento:
        db.delete(alimento)
        db.commit()
        return True
    return  False


def deletarPrato(db: Session, prato_id):
    prato = buscarPratoPorId(db, prato_id)
    if prato:
        db.delete(prato)
        db.commit()
        return True
    return  False
