from sqlalchemy.orm import Session
from api.modules.moduloPrato import gerarRefeicao

from random import randint


def gerarMenu(alimentos: list):
    prato_cafeManha = gerarRefeicao(alimentos, "Café da Manhã")
    prato_almoco = gerarRefeicao(alimentos, "Almoço")
    prato_jantar = gerarRefeicao(alimentos, "Jantar")

    cardapio_dia_dict = {
        "Café da Manhã": prato_cafeManha, 
        "Almoço": prato_almoco, 
        "Jantar": prato_jantar}

    return cardapio_dia_dict


