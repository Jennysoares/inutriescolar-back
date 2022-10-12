from sqlalchemy.orm import Session
from api.modules.moduloPrato import gerarDesjejum, gerarAlmoco, gerarJanta, gerarLanche

from random import randint


def gerarMenu(db: Session):
    prato_desjejum = gerarDesjejum(db=db)
    prato_almoco = gerarAlmoco(db=db)
    prato_lanche = gerarLanche(db=db)
    prato_jantar = gerarJanta(db=db)

    cardapio_dia_dict = {"Desjejum": prato_desjejum, "Almoço": prato_almoco, "Lanche": prato_lanche, "Jantar": prato_jantar}

    return cardapio_dia_dict
