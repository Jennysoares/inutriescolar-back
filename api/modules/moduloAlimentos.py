from sqlalchemy.orm import Session
from api.model.querysBusca import buscarComidaPorId, buscarCriacao
 

def plates(prato, db: Session):

    alimentos = buscarCriacao(db=db, id_prato=prato.id)
    alimentos_prato = []

    for i in range(len(alimentos)):
        alimentos_prato.append(buscarComidaPorId(db=db, id_alimento=alimentos[i].id_alimento))

    return alimentos_prato
