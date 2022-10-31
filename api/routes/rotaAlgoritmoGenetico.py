from fastapi import FastAPI, APIRouter, Depends
from api.model.crud import buscarTodosAlimentos
from api.model.querysBusca import buscarReferencial, buscarTodasCriacoes
from api.modules.moduloAlgoritmoGenetico import funcao_roleta, funcao_torneio, gerar_populacao, calcularCusto, funcao_fitness, funcao_dizimacao_corte, funcao_dizimacao_pais, cruzamento, mutacao
from sqlalchemy.orm import Session
from api.model.database import SessionLocal, engine
import timeit

from api.modules.moduloPrato import retornaPratosParametros

algoritmo = APIRouter()

taxa_mutacao = 0.1
taxa_cruzamento = 0.8


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def gerarCardapioAG(numIndividuos: int, qtd_dias: int, escolaridade: int, tipoSelecao: int, alergia: str, db: Session = Depends(get_db)):
    inicio = timeit.default_timer()
    populacao = []  
    referencial = buscarReferencial(db, escolaridade)[0]
    pratos = retornaPratosParametros(alergia, db)
    listaDeTodosAlimentos = buscarTodosAlimentos(db)
    listaDeTodasCriacoes = buscarTodasCriacoes(db)
    
    for _ in range(numIndividuos):
        populacao = gerar_populacao(numIndividuos, qtd_dias, pratos)
    
    geracao_atual = populacao
    fitness = funcao_fitness(populacao, 1, escolaridade, referencial, listaDeTodosAlimentos, listaDeTodasCriacoes)
    print(f'Fitness geração inicial = {fitness}')

    custo = dict()
    indices = 0
    while True:
        custo.update({round(calcularCusto(geracao_atual[indices], referencial), 2): indices})
        indices += 1
        if indices == numIndividuos:
            break

    print(f'\nCusto geração inicial = {custo}')

    for i in range(0, 1):
        nova_populacao = []
        corte_populacao = []

        if tipoSelecao == 1:
            corte_populacao = funcao_dizimacao_corte(populacao, escolaridade, referencial, listaDeTodosAlimentos, listaDeTodasCriacoes)

        while len(nova_populacao) != numIndividuos:
            pais = []
            if tipoSelecao == 1:
                pais = funcao_dizimacao_pais(corte_populacao)
            elif tipoSelecao == 2:
                pais = funcao_roleta(populacao, escolaridade, referencial, listaDeTodosAlimentos, listaDeTodasCriacoes)
            elif tipoSelecao == 3:
                pais = funcao_torneio(populacao, escolaridade, referencial, listaDeTodosAlimentos, listaDeTodasCriacoes)

            filhos_gerados = cruzamento(pais, taxa_cruzamento)
            filhos_mutados = mutacao(filhos_gerados, taxa_mutacao, pratos)
            nova_populacao.append(filhos_mutados[0])
            nova_populacao.append(filhos_mutados[1])

            if len(nova_populacao) > numIndividuos:
                nova_populacao.pop()

        geracao_atual = nova_populacao
    fim = timeit.default_timer()
    print(f'\nTempo de execução: {fim - inicio}')

    fitnessFinal = funcao_fitness(geracao_atual, 1, escolaridade, referencial, listaDeTodosAlimentos, listaDeTodasCriacoes)
    print(f'\nFitness geração Final = {fitnessFinal}')

    return geracao_atual
        
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

