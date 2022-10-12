from fastapi import FastAPI, APIRouter, Depends
from api.modules.moduloAlgoritmoGenetico import funcao_roleta, funcao_torneio, gerar_populacao, calcularCusto, funcao_fitness, funcao_dizimacao_corte, funcao_dizimacao_pais, cruzamento, mutacao
from sqlalchemy.orm import Session
from api.model.database import SessionLocal, engine
import timeit

algoritmo = APIRouter()

taxa_mutacao = 0.5
taxa_cruzamento = 0.8


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def gerarCardapioAG(numIndividuos: int, qtd_dias: int, escolaridade: int, tipoSelecao: int, db: Session = Depends(get_db)):
    inicio = timeit.default_timer()
    populacao = []  

    for _ in range(numIndividuos):
        populacao = gerar_populacao(numIndividuos, qtd_dias, db)

    fitness = funcao_fitness(populacao, 2, escolaridade, db)
    print(f'Fitness geração inicial = {fitness}')

    # custo = dict()
    # indices = 0
    # while True:
    #     custo.update({round(calcularCusto(geracao_atual[indices]), 2): indices})
    #     indices += 1
    #     if indices == numIndividuos:
    #         break

    # print(f'Custo geração inicial = {custo}')

    for _ in range(0, 500):
        nova_populacao = []
        corte_populacao = []

        if tipoSelecao == 1:
            corte_populacao = funcao_dizimacao_corte(populacao, escolaridade, db)

        for k in range(0, int(numIndividuos / 2)):
            pais = []
            if tipoSelecao == 1:
                pais = funcao_dizimacao_pais(corte_populacao)
            elif tipoSelecao == 2:
                pais = funcao_roleta(populacao)
            elif tipoSelecao == 3:
                pais = funcao_torneio(populacao)

            filhos_gerados = cruzamento(pais, taxa_cruzamento)
            filhos_mutados = mutacao(filhos_gerados, taxa_mutacao, db)
            nova_populacao.append(filhos_mutados[0])
            nova_populacao.append(filhos_mutados[1])

        geracao_atual = nova_populacao

    fim = timeit.default_timer()
    print(f'\nTempo de execução: {fim - inicio}')

    return geracao_atual
        
@algoritmo.get("/genetic/dizimacao/{numIndividuos}/{qtd_dias}/{escolaridade}")
def algoritmo_genetico(numIndividuos: int, qtd_dias: int, escolaridade: int, db: Session = Depends(get_db)):
    
    populacao = gerarCardapioAG(numIndividuos, qtd_dias, escolaridade, 1, db)
    return populacao


@algoritmo.get("/genetic/torneio/{numIndividuos}/{qtd_dias}/{escolaridade}")
def algoritmo_genetico(numIndividuos: int, qtd_dias: int, escolaridade: int, db: Session = Depends(get_db)):

    populacao = gerarCardapioAG(numIndividuos, qtd_dias, escolaridade, 3, db)
    return populacao


@algoritmo.get("/genetic/roleta/{numIndividuos}/{qtd_dias}/{escolaridade}")
def algoritmo_genetico(numIndividuos: int, qtd_dias: int, escolaridade: int, db: Session = Depends(get_db)):

    populacao = gerarCardapioAG(numIndividuos, qtd_dias, escolaridade, 2, db)
    return populacao

