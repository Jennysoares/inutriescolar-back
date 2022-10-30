from sqlalchemy.orm import Session

from . import models, schemas


def buscarPratoPorArrayCategorias(db: Session, categorias: list):
    return db.query(models.Prato).filter(models.Prato.categoria.in_(categorias)).all()

def buscarTodosPrato(db: Session):
    return db.query(models.Prato).all()

def buscarPrato(db: Session, categoria: str):
    return db.query(models.Prato).filter(models.Prato.categoria == categoria).all()

def bucarIdsAlimentosExcecao(db: Session, query: str):
    ids = []
    idAlimentosExcecao = db.execute(query).fetchall()
    for row in idAlimentosExcecao:
        row_as_dict = dict(row)
        ids.append(row_as_dict['id'])
    return ids


def buscarIdsCombinacaoExcecao(db: Session, idsAlimentoExcecao: list):
    ids = []
    idsCombinacao = db.query(models.Criacao.id_prato).distinct(models.Criacao.id_prato).filter(models.Criacao.id_alimento.in_(idsAlimentoExcecao)).all()
    for row in idsCombinacao:
        ids.append(row.id_prato)
    return ids
    
def buscarPratosExcecao(db: Session, idsCombinacaoExcecao: list):
    return db.query(models.Prato).filter(models.Prato.id.notin_(idsCombinacaoExcecao)).all()

def buscarComidaPorGrupo(db: Session, grupo: str):
    return db.query(models.Alimento).filter(models.Alimento.grupo == grupo).all()

def buscarTodasCriacoes(db: Session):
    return db.query(models.Criacao).all()

def buscarCriacao(db: Session, id_prato: int):
    return db.query(models.Criacao).filter(models.Criacao.id_prato == id_prato).all()


def buscarComidaPorId(db: Session, id_alimento: int):
    return db.query(models.Alimento).filter(models.Alimento.id == id_alimento).all()

def buscarTodasComidas(db: Session):
    return db.query(models.Alimento).all()

def buscarComidaPorGrupoDeIds(db: Session, id_alimento: list):
    return db.query(models.Alimento).filter(models.Alimento.id.in_(id_alimento)).all()


def buscarReferencial(db: Session, escolaridade: int):
    return db.query(models.ReferencialNutrientes).filter(models.ReferencialNutrientes.escolaridade == escolaridade).all()
