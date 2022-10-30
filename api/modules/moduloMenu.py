from sqlalchemy.orm import Session
from api.modules.moduloPrato import gerarCafeManha, gerarAlmoco, gerarJanta

from random import randint


def gerarMenu(alergia: str , db: Session):
    prato_cafeManha = gerarCafeManha(alergia, db=db)
    prato_almoco = gerarAlmoco(alergia, db=db)
    prato_jantar = gerarJanta(alergia, db=db)

    cardapio_dia_dict = {"Café da Manhã": prato_cafeManha, "Almoço": prato_almoco, "Jantar": prato_jantar}

    return cardapio_dia_dict
