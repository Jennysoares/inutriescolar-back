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

def retornaPratosParametros(alergia: str, db: Session):
    pratos = []

    if "0" in alergia:
        pratos = buscarTodosPrato(db)
    else:
        query = montarQueryAlimentosExcecao(alergia)
        idAlimentosExcecao = bucarIdsAlimentosExcecao(db, query)
        idsCombinacaoExcecao = buscarIdsCombinacaoExcecao(db, idAlimentosExcecao)
        pratos = buscarPratosExcecao(db, idsCombinacaoExcecao)

    return pratos

def buscarPratosCardapio(refeicao: str, pratos: list, refeicaoEspecifica: str = None): 
    lista_refeicoes = []

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


def gerarRefeicao(alimentos: list, refeicao: str):
    prato_refeicao = []
    pratos_refeicao = buscarPratosCardapio(refeicao, alimentos)

    for i in range(len(pratos_refeicao)):
        tam = len(pratos_refeicao[i])
        aux = randint(0, tam - 1)

        prato_refeicao.append(pratos_refeicao[i][aux])

    return prato_refeicao