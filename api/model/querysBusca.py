from sqlalchemy.orm import Session

from . import models, schemas


def buscarPratoPorArrayCategorias(db: Session, categorias: list):
    return db.query(models.Prato).filter(models.Prato.categoria.in_(categorias)).all()

def buscarPrato(db: Session, categoria: str):
    return db.query(models.Prato).filter(models.Prato.categoria == categoria).all()


def buscarComidaPorGrupo(db: Session, grupo: str):
    return db.query(models.Alimento).filter(models.Alimento.grupo == grupo).all()


def buscarCriacao(db: Session, id_prato: int):
    return db.query(models.Criacao).filter(models.Criacao.id_prato == id_prato).all()


def buscarComidaPorId(db: Session, id_alimento: int):
    return db.query(models.Alimento).filter(models.Alimento.id == id_alimento).all()


def buscarComidaPorGrupoDeIds(db: Session, id_alimento: list):
    return db.query(models.Alimento).filter(models.Alimento.id.in_(id_alimento)).all()


def buscarReferencial(db: Session, escolaridade: int):
    return db.query(models.ReferencialNutrientes).filter(models.ReferencialNutrientes.escolaridade == escolaridade).all()
