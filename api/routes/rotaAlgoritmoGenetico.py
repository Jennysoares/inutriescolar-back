from fastapi import APIRouter, Depends
from api.model.crud import buscarTodosAlimentos
from api.model.querysBusca import buscarReferencial, buscarTodasCriacoes
from api.modules.moduloAlgoritmoGenetico import funcao_roleta_criacao, funcao_roleta_pais, funcao_torneio, gerar_populacao, calcularCusto, funcao_fitness, funcao_dizimacao_corte, funcao_dizimacao_pais, cruzamento, mutacao
from sqlalchemy.orm import Session
from api.model.database import SessionLocal
import timeit

from api.modules.moduloPrato import retornaPratosParametros

algoritmo = APIRouter()

taxa_mutacao = 0.4
taxa_cruzamento = 0.8


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def gerarCardapioAG(numIndividuos: int, qtd_dias: int, escolaridade: int, tipoSelecao: int, alergia: str, db: Session = Depends(get_db), populacaoRecebida = None):
    populacao = []  
    referencial = buscarReferencial(db, escolaridade)[0]
    pratos = retornaPratosParametros(alergia, db)
    listaDeTodosAlimentos = buscarTodosAlimentos(db)
    listaDeTodasCriacoes = buscarTodasCriacoes(db)
    geracoes = 50
    
    if populacaoRecebida == None:
        for _ in range(numIndividuos):
            populacao = gerar_populacao(numIndividuos, qtd_dias, pratos)
    else:
        populacao = populacaoRecebida
    
    geracao_atual = populacao 

    i = 0
    while i != geracoes:
        nova_populacao = []
        corte_populacao = []
        fitness = []
        roleta = []

        if tipoSelecao == 1:
            corte_populacao = funcao_dizimacao_corte(geracao_atual, escolaridade, referencial, listaDeTodosAlimentos, listaDeTodasCriacoes)
        elif tipoSelecao == 2:
            roleta = funcao_roleta_criacao(geracao_atual, escolaridade, referencial, listaDeTodosAlimentos, listaDeTodasCriacoes)
        elif tipoSelecao == 3:
            fitness = funcao_fitness(geracao_atual, escolaridade, referencial, listaDeTodosAlimentos, listaDeTodasCriacoes)    

        while len(nova_populacao) != numIndividuos:
            pais = []
            if tipoSelecao == 1:
                pais = funcao_dizimacao_pais(corte_populacao)
            elif tipoSelecao == 2:
                pais = funcao_roleta_pais(geracao_atual, roleta)
            elif tipoSelecao == 3:
                pais = funcao_torneio(geracao_atual, fitness)

            filhos_gerados = cruzamento(pais, taxa_cruzamento)
            filhos_mutados = mutacao(filhos_gerados, taxa_mutacao, pratos)
            nova_populacao.append(filhos_mutados[0])
            nova_populacao.append(filhos_mutados[1])

            if len(nova_populacao) > numIndividuos:
                nova_populacao.pop()

        geracao_atual = nova_populacao
        i+= 1

    return geracao_atual

def gerarCardapioAGComparacao(qtdGeracao: int ,numIndividuos: int, escolaridade: int, tipoSelecao: int,  populacaoRecebida: list, fitnessInicial: dict, 
referencial: list, pratos: list, listaDeTodosAlimentos: list, listaDeTodasCriacoes: list ):
    inicio = timeit.default_timer()
    populacao = populacaoRecebida 
    
    geracao_atual = populacao
    
    i = 0
    while i != qtdGeracao:
        nova_populacao = []
        corte_populacao = []
        fitness = []
        roleta = []

        if tipoSelecao == 1:
            corte_populacao = funcao_dizimacao_corte(geracao_atual, escolaridade, referencial, listaDeTodosAlimentos, listaDeTodasCriacoes)
        elif tipoSelecao == 2:
            roleta = funcao_roleta_criacao(geracao_atual, escolaridade, referencial, listaDeTodosAlimentos, listaDeTodasCriacoes)
        elif tipoSelecao == 3:
            fitness = funcao_fitness(geracao_atual, escolaridade, referencial, listaDeTodosAlimentos, listaDeTodasCriacoes)    

        while len(nova_populacao) != numIndividuos:
            pais = []
            if tipoSelecao == 1:
                pais = funcao_dizimacao_pais(corte_populacao)
            elif tipoSelecao == 2:
                pais = funcao_roleta_pais(geracao_atual, roleta)
            elif tipoSelecao == 3:
                pais = funcao_torneio(geracao_atual, fitness)

            filhos_gerados = cruzamento(pais, taxa_cruzamento)
            filhos_mutados = mutacao(filhos_gerados, taxa_mutacao, pratos)
            nova_populacao.append(filhos_mutados[0])
            nova_populacao.append(filhos_mutados[1])

            if len(nova_populacao) > numIndividuos:
                nova_populacao.pop()

        geracao_atual = nova_populacao
        i+= 1
    fim = timeit.default_timer()
    fitnessFinal = funcao_fitness(geracao_atual, escolaridade, referencial, listaDeTodosAlimentos, listaDeTodasCriacoes)    

    print(f'Quantidade de indivíduos/cardápios: {len(geracao_atual)}')
    print(f'Quantidade de gerações realizadas: {qtdGeracao}')
    print(f'Média do Fitness geração inicial = {sum(fitnessInicial.values()) / len(fitnessInicial):.2f}')
    print(f'Média do Fitness geração Final = {sum(fitnessFinal.values()) / len(fitnessFinal):.2f}')
    print(f'Tempo de execução: {fim - inicio:.2f}\n')


    return geracao_atual

@algoritmo.get("/compararMetodos/{qtdGeracao}/{numIndividuos}/{qtd_dias}/{escolaridade}/{alergia}/")
def algoritmo_genetico(qtdGeracao: int, numIndividuos: int, qtd_dias: int, escolaridade: int, alergia: str, db: Session = Depends(get_db)):
    referencial = buscarReferencial(db, escolaridade)[0]
    pratos = retornaPratosParametros(alergia, db)
    listaDeTodosAlimentos = buscarTodosAlimentos(db)
    listaDeTodasCriacoes = buscarTodasCriacoes(db)
    populacao = []

    for _ in range(numIndividuos):
            populacao = gerar_populacao(numIndividuos, qtd_dias, pratos)

    fitnessInicial = funcao_fitness(populacao, escolaridade, referencial, listaDeTodosAlimentos, listaDeTodasCriacoes)    

    print(f'\n========== MÉTODO DE SELEÇÃO: DIZIMAÇÃO ==========')
    gerarCardapioAGComparacao(qtdGeracao, numIndividuos, escolaridade, 1, populacao, fitnessInicial, referencial, pratos, listaDeTodosAlimentos, listaDeTodasCriacoes)
    print(f'========== MÉTODO DE SELEÇÃO: ROLETA ==========')
    gerarCardapioAGComparacao(qtdGeracao, numIndividuos, escolaridade, 2, populacao, fitnessInicial, referencial, pratos, listaDeTodosAlimentos, listaDeTodasCriacoes)
    print(f'========== MÉTODO DE SELEÇÃO: TORNEIO ==========')
    gerarCardapioAGComparacao(qtdGeracao, numIndividuos, escolaridade, 3, populacao, fitnessInicial, referencial, pratos, listaDeTodosAlimentos, listaDeTodasCriacoes)


@algoritmo.get("/dizimacao/{numIndividuos}/{qtd_dias}/{escolaridade}/{alergia}")
def algoritmo_genetico(numIndividuos: int, qtd_dias: int, escolaridade: int, alergia: str, db: Session = Depends(get_db)):
    
    populacao = gerarCardapioAG(numIndividuos, qtd_dias, escolaridade, 1, alergia, db)
    return {"menu": populacao }


@algoritmo.get("/torneio/{numIndividuos}/{qtd_dias}/{escolaridade}/{alergia}")
def algoritmo_genetico(numIndividuos: int, qtd_dias: int, escolaridade: int, alergia: str, db: Session = Depends(get_db)):

    populacao = gerarCardapioAG(numIndividuos, qtd_dias, escolaridade, 3, alergia, db)
    return {"menu": populacao }


@algoritmo.get("/roleta/{numIndividuos}/{qtd_dias}/{escolaridade}/{alergia}")
def algoritmo_genetico(numIndividuos: int, qtd_dias: int, escolaridade: int, alergia: str, db: Session = Depends(get_db)):

    populacao = gerarCardapioAG(numIndividuos, qtd_dias, escolaridade, 2, alergia, db)
    return {"menu": populacao }

