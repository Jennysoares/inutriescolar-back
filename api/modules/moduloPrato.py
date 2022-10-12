from sqlalchemy.orm import Session
from api.model.querysBusca import buscarPratoPorArrayCategorias, buscarPrato

from random import randint

def retornaListaDePratosPorCategoriaRefeicao(refeicao: str,  categoria: str, db: Session):
    if refeicao == "Lanche" and (categoria == "Bebidas" or categoria == "Suco"):
        return buscarPrato(db, "Bebidas") + buscarPrato(db, "Suco")
    else:
        return buscarPrato(db, categoria)

def gerarPrato(refeicao: str, db: Session):
    lista_refeicoes = []
    categorias = []

    if refeicao == "Desjejum":
        categorias = ["Frutas", "Pão/Cereal", "Leite ou derivados"]

    elif refeicao == "Lanche":
        categorias = ["Frutas", "Bebidas", "Suco", "Pão/Cereal"]
        
        pratos = buscarPratoPorArrayCategorias(db, categorias)
        lista_refeicoes.append([x for x in pratos if x.categoria == "Frutas"])
        lista_refeicoes.append([x for x in pratos if x.categoria == "Bebidas" or x.categoria == "Suco"])
        lista_refeicoes.append([x for x in pratos if x.categoria == "Pão/Cereal"])

        return lista_refeicoes

    elif refeicao == "Almoço" or refeicao == "Jantar":
        categorias = ["Acomp Arroz", "Acomp Feijão", "Entrada", "Guarnição", "Principal", "Sobremesa", "Suco"]

    else:
        return "Nao existe o tipo de refeicao desejado!"


    pratos = buscarPratoPorArrayCategorias(db, categorias)
    for tipoRefeicao in categorias:
        lista_refeicoes.append([x for x in pratos if x.categoria == tipoRefeicao])


    return lista_refeicoes


def gerarDesjejum(db: Session):
    prato_desjejum = []

    pratos_desjejum = gerarPrato("Desjejum", db=db)

    for i in range(len(pratos_desjejum)):
        tam = len(pratos_desjejum[i])
        aux = randint(0, tam - 1)

        prato_desjejum.append(pratos_desjejum[i][aux])

    return prato_desjejum


def gerarAlmoco(db: Session):
    prato_almoco = []

    pratos_almoco = gerarPrato("Almoço", db=db)

    for i in range(len(pratos_almoco)):
        tam = len(pratos_almoco[i])
        aux = randint(0, tam - 1)

        prato_almoco.append(pratos_almoco[i][aux])

    return prato_almoco


def gerarLanche(db: Session):
    prato_lanche = []

    pratos_lanche = gerarPrato("Lanche", db=db)

    for i in range(len(pratos_lanche)):
        tam = len(pratos_lanche[i])
        aux = randint(0, tam - 1)

        prato_lanche.append(pratos_lanche[i][aux])

    return prato_lanche


def gerarJanta(db: Session):
    prato_jantar = []

    pratos_jantar = gerarPrato("Jantar", db=db)

    for i in range(len(pratos_jantar)):
        tam = len(pratos_jantar[i])
        aux = randint(0, tam - 1)

        prato_jantar.append(pratos_jantar[i][aux])

    return prato_jantar
