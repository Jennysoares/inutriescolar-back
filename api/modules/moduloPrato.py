from sqlalchemy.orm import Session
from api.model.querysBusca import bucarIdsAlimentosExcecao,  buscarIdsCombinacaoExcecao, buscarPratosExcecao, buscarTodosPrato

from random import randint

categorias = {
        "Café da Manhã": ["Frutas", "Bebidas", "Leite ou derivados", "Pão/Cereal"], 
        "Almoço": ["Acompanhamento Arroz", "Acompanhamento Feijão", "Guarnição", "Principal", "Suco", "Sobremesa"],
        "Jantar": ["Acompanhamento Arroz", "Acompanhamento Feijão", "Guarnição", "Principal", "Suco", "Sobremesa"]
        }

def montarQueryAlimentosExcecao(alergia: str):
    flagGrupo = 0
    flagNome = 0

    queryAlimentos = 'select id from alimentos a where'
    queryGrupo = ' a.grupo in ('
    queryNomes = " "

    if "1" in alergia:
        queryGrupo += "'Ovos e derivados'"
        queryNomes += "lower(a.nome) like '%ovo%'"
        flagNome = 1
        flagGrupo = 1
    if "2" in alergia:
        if flagNome == 1 and flagGrupo == 1:
            queryGrupo += ", 'Leite e derivados')"
            queryNomes += " or lower(a.nome) like '%leite%'"
        else:
            queryGrupo += 'Leite e derivados)'
            queryNomes += "lower(a.nome) like '%leite%'"
            flagNome = 1
            flagGrupo = 1
    if "3" in alergia:
        if flagNome == 1:
            queryNomes += " or lower(a.nome) like '%soja%'"
        else:
            queryNomes += "lower(a.nome) like '%soja%'"
            flagNome = 1
    if "4" in alergia:
        if flagNome == 1:
            queryNomes += " or lower(a.nome) like '%trigo%'"
        else:
            queryNomes += "lower(a.nome) like '%trigo%'"
            flagNome = 1

    if flagGrupo == 1:
        queryAlimentos += queryGrupo
    if flagNome == 1:
        if flagGrupo == 1:
            queryAlimentos += " and"
        queryAlimentos += queryNomes

    return queryAlimentos

def buscarPratosCardapio(refeicao: str, alergia: str, db: Session, refeicaoEspecifica: str = None): 
    lista_refeicoes = []
    pratos = []

    if "0" in alergia:
        pratos = buscarTodosPrato(db)
    else:
        query = montarQueryAlimentosExcecao(alergia)
        idAlimentosExcecao = bucarIdsAlimentosExcecao(db, query)
        idsCombinacaoExcecao = buscarIdsCombinacaoExcecao(db, idAlimentosExcecao)
        pratos = buscarPratosExcecao(db, idsCombinacaoExcecao)

    if refeicao  == "Café da Manhã":
        lista_refeicoes.append([x for x in pratos if x.categoria == "Frutas"])
        lista_refeicoes.append([x for x in pratos if x.categoria == "Leite ou derivados" or x.categoria == "Bebidas"])
        lista_refeicoes.append([x for x in pratos if x.categoria == "Pão/Cereal"])
    else:
        for tipoRefeicao in categorias[refeicao]:
            lista_refeicoes.append([x for x in pratos if x.categoria == tipoRefeicao])   

    if refeicaoEspecifica is not None:
        if refeicao == 'Café da Manhã' and (refeicaoEspecifica == 'Bebidas' or refeicaoEspecifica == 'Leite ou derivados'):
            index = 1        
        else:
            index = categorias[refeicao].index(refeicaoEspecifica) - 1

        return lista_refeicoes[index]
    else:
        return lista_refeicoes


def gerarCafeManha(alergia: str, db: Session):
    prato_cafeManha = []
    pratos_cafeManha = buscarPratosCardapio("Café da Manhã", alergia, db=db)

    for i in range(len(pratos_cafeManha)):
        tam = len(pratos_cafeManha[i])
        aux = randint(0, tam - 1)

        prato_cafeManha.append(pratos_cafeManha[i][aux])

    return prato_cafeManha


def gerarAlmoco(alergia: str, db: Session):
    prato_almoco = []
    pratos_almoco = buscarPratosCardapio("Almoço", alergia, db=db)
    for i in range(len(pratos_almoco)):
        tam = len(pratos_almoco[i])
        aux = randint(0, tam - 1)

        prato_almoco.append(pratos_almoco[i][aux])
    return prato_almoco


def gerarLanche(alergia: str, db: Session):
    prato_lanche = []

    pratos_lanche = buscarPratosCardapio("Lanche", alergia, db=db)

    for i in range(len(pratos_lanche)):
        tam = len(pratos_lanche[i])
        aux = randint(0, tam - 1)

        prato_lanche.append(pratos_lanche[i][aux])

    return prato_lanche


def gerarJanta(alergia: str, db: Session):
    prato_jantar = []

    pratos_jantar = buscarPratosCardapio("Jantar", alergia, db=db)

    for i in range(len(pratos_jantar)):
        tam = len(pratos_jantar[i])
        aux = randint(0, tam - 1)

        prato_jantar.append(pratos_jantar[i][aux])

    return prato_jantar
