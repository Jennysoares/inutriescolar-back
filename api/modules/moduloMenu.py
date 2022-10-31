from sqlalchemy.orm import Session
from api.modules.moduloPrato import gerarCafeManha, gerarAlmoco, gerarJanta

from random import randint


def gerarMenu(alimentos: list):
    prato_cafeManha = gerarCafeManha(alimentos)
    prato_almoco = gerarAlmoco(alimentos)
    prato_jantar = gerarJanta(alimentos)

    cardapio_dia_dict = {"Café da Manhã": prato_cafeManha, "Almoço": prato_almoco, "Jantar": prato_jantar}

    return cardapio_dia_dict
