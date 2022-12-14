from api.modules.moduloMenu import gerarMenu
from sqlalchemy.orm import Session
import random
from operator import itemgetter

def gerar_populacao(tam_pop, qtdDias, alimentos):
    populacao = []   

    for i in range(tam_pop):
        cardapioDia = []
        for j in range(qtdDias):
            individuo = gerarMenu(alimentos)
            cardapioDia.append(individuo)
        populacao.append(cardapioDia)

    return populacao

def funcao_fitness(populacao, escolaridade, referencial, listaDeAlimentos, listaDeCriacoes):
    fitness_valores = dict()

    for i in range(0, len(populacao)):
        fitness = funcao_objetivo(populacao[i], escolaridade, referencial, listaDeAlimentos, listaDeCriacoes)
        fitness_valores[i] = fitness

    return fitness_valores


def funcao_objetivo(cardapio, escolaridade, referencial, listaDeAlimentos, listaDeCriacoes):    
    f1 = calcularErroNutri(cardapio, escolaridade, referencial, listaDeAlimentos, listaDeCriacoes)
    f2 = calcularCusto(cardapio,  referencial)

    aptidao = (0.6 * f1) + (0.4 * f2)
    aptidao = round(aptidao, 3)

    return aptidao

def buscarComidaPorIds(listaDeAlimentos:list, ids: list):
    return [x for x in listaDeAlimentos if x.id in ids]

def buscarCriacaoPorIds(listaDeCriacoes:list, id: int):
    return [x for x in listaDeCriacoes if x.id == id]


def calcularErroNutri(cardapio, escolaridadeId, referencial, listaDeAlimentos, listaDeCriacoes):
    nutriCardapio = dict(energia=0,
                         proteinas=0,
                         lipideos=0,
                         carboidratos=0,
                         fibras=0,
                         calcio=0,
                         magnesio=0,
                         ferro=0,
                         zinco=0)

    for dia in cardapio:
        for refeicao in dia:
            for pratos in dia[refeicao]:
                criacao = buscarCriacaoPorIds(listaDeCriacoes, pratos.id)
                ids = [element.id_alimento for element in criacao]
                alimentosDoPrato = buscarComidaPorIds(listaDeAlimentos, ids)
                for ingrediente in criacao:
                    alimento = next(x for x in alimentosDoPrato if x.id == ingrediente.id_alimento )
                    for nutriente in alimento.__dict__ :
                        if nutriente in nutriCardapio.keys():
                            valorPrato = 0
                            if escolaridadeId == 1:
                                valorPrato = (alimento.__dict__[nutriente] * ingrediente.qtdEnsinoCreche) / 100
                            elif escolaridadeId == 2:
                                valorPrato = (alimento.__dict__[nutriente] * ingrediente.qtdEnsinoFun1) / 100
                            elif escolaridadeId == 3:
                                valorPrato = (alimento.__dict__[nutriente] * ingrediente.qtdEnsinoFun2) / 100
                            elif escolaridadeId == 4:
                                valorPrato = (alimento.__dict__[nutriente] * ingrediente.qtdEnsinoMedio) / 100

                            valor = nutriCardapio[nutriente] + valorPrato
                            nutriCardapio[nutriente] = valor

    # Restri????o das cores

    coreslist = list()
    for dia in cardapio:
        for refeicao in dia:
            cores = dict(Amarelo=0, Vermelho=0, Verde=0, Marrom=0, Branco=0, Laranja=0)
            for pratos in dia[refeicao]:
                if pratos.categoria in ["Entrada", "Guarni????o", "Sobremesa", "Bebidas"]:
                    if pratos.cor == 'Amarelo':
                        cores['Amarelo'] += 1
                    if pratos.cor == 'Vermelho':
                        cores['Vermelho'] += 1
                    if pratos.cor == 'Verde':
                        cores['Verde'] += 1
                    if pratos.cor == 'Marrom':
                        cores['Marrom'] += 1
                    if pratos.cor == 'Branco':
                        cores['Branco'] += 1
                    if pratos.cor == 'Laranja':
                        cores['Laranja'] += 1
            coreslist.append(cores)

    restricaoCor = 0
    for cor in coreslist:
        if cor['Amarelo'] > 2:
            r1 = (cor['Amarelo'] - 2)
            restricaoCor += r1
        if cor['Vermelho'] > 2:
            r1 = (cor['Vermelho'] - 2)
            restricaoCor += r1
        if cor['Verde'] > 2:
            r1 = (cor['Verde'] - 2)
            restricaoCor += r1
        if cor['Marrom'] > 2:
            r1 = (cor['Marrom'] - 2)
            restricaoCor += r1
        if cor['Branco'] > 2:
            r1 = (cor['Branco'] - 2)
            restricaoCor += r1
        if cor['Laranja'] > 2:
            r1 = (cor['Laranja'] - 2)
            restricaoCor += r1

    # Restri????o Consistencia

    liqpas = 0
    for dia in cardapio:
        for refeicao in dia:
            for pratos in dia[refeicao]:
                if pratos.categoria in ["Acompanhamento Feij??o", "Guarni????o", "Principal"]:
                    if pratos.consistencia == 'Liqu??da' or pratos.consistencia == 'Pastosa':
                        liqpas += 1

    if liqpas > 1:
        restricaoConsistencia = liqpas
    else:
        restricaoConsistencia = 0


    # Restri????o Variedade

    restricaoRepeticao = 0
    for dia in cardapio:
        for pratoAlmoco in dia['Almo??o']:
            if pratoAlmoco.categoria in ["Entrada","Guarni????o", "Principal", "Sobremesa", "Bebidas"]:
                if pratoAlmoco in dia['Jantar']:
                    restricaoRepeticao += 1

    indice = 0
    listIndRepet = list()
    for dia in cardapio:
        for diaComparacao in range(0, len(cardapio)):
            if indice != diaComparacao:
                for pratoAlmoco in dia['Almo??o']:
                    if pratoAlmoco.categoria in ["Entrada","Guarni????o", "Principal"]:
                        if pratoAlmoco in cardapio[diaComparacao]['Jantar']:
                            if diaComparacao + indice not in listIndRepet:
                                listIndRepet.append(diaComparacao + indice)
        indice += 1

    restricaoRepeticao += len(listIndRepet)

    for chave in nutriCardapio:
        valor = nutriCardapio[chave]
        valor = referencial.__dict__[chave] - valor
        nutriCardapio[chave] = abs(valor)

    erroInicial = 0

    for chave in nutriCardapio:
        erroInicial += abs(nutriCardapio[chave])

    erroInicial = erroInicial / len(nutriCardapio)

    totalRestricoes = restricaoCor + restricaoConsistencia + (restricaoRepeticao * 2)
    erroFinal = erroInicial + totalRestricoes
    return erroFinal


def calcularCusto(cardapio, referencial):
    custoCardapio = 0
    w = 0

    for dia in cardapio:
        for refeicao in dia:
            for pratos in dia[refeicao]:
                custoCardapio += float(pratos.valor)

    if custoCardapio > referencial.custoAluno:
        w = 1

    penalidade = w * referencial.custoAluno

    return custoCardapio + penalidade

def funcao_roleta_criacao(pop, escolaridade, referencial, listaDeAlimentos, listaDeCriacoes):
    fitnessCandidatos = funcao_fitness(pop, escolaridade, referencial, listaDeAlimentos, listaDeCriacoes) 
    fitnessOrdenado = dict(sorted(fitnessCandidatos.items(), key=itemgetter(1))) 
    fitnessTotal = round(sum(fitnessOrdenado.values()))
    roletaCandidatos = {}
    proporcaoInicial = 0
    for indiceCandidato in fitnessOrdenado.keys():
        proporcaoFinal = round(fitnessOrdenado[indiceCandidato]) * 100 / fitnessTotal
        if proporcaoInicial == proporcaoFinal:
              proporcaoFinal += 0.1

        roletaCandidatos.update({indiceCandidato: [proporcaoInicial, proporcaoFinal]})
        proporcaoInicial = proporcaoFinal    

    
    return roletaCandidatos     

def funcao_roleta_pais(pop, roletaCandidatos):
    pais = list()
    pai1 = random.uniform(0, roletaCandidatos[len(pop)-1][1]- 0.1)
    indicePai1 = 0
    for item in roletaCandidatos.values():
        if (pai1 >= item[0] and pai1 < item[1]):
            indicePai1 = list(roletaCandidatos.keys())[list(roletaCandidatos.values()).index(item)]
            pais.append(pop[indicePai1])
            break
    
    pai2 = random.uniform(0, roletaCandidatos[len(pop)-1][1]- 0.1)
    indicePai2 = 0
    for item in roletaCandidatos.values():
        if (pai2 >= item[0] and pai2 < item[1]):
            indicePai2 = list(roletaCandidatos.keys())[list(roletaCandidatos.values()).index(item)]
            pais.append(pop[indicePai2])
            break    
    return pais  

    
def funcao_torneio(pop, fitness):
    populacao = list(pop[:])
    tamanhoPopulacao = len(populacao)
    qtdPopulacaoTorneio = int(tamanhoPopulacao * 0.6)
    paisSelecionados = list()
    fitnessCandidatos = {}
    primeiroGanhador = -1
    
    while len(paisSelecionados) != 2:
        cromossomosCanditados = list()
        fitnessCandidatos = {}

        while len(cromossomosCanditados) != qtdPopulacaoTorneio:
            indiceCanditado = random.randint(0, len(populacao) - 1)    
            if (indiceCanditado not in cromossomosCanditados) and (indiceCanditado != primeiroGanhador):
                cromossomosCanditados.append(indiceCanditado)
                fitnessCandidatos.update({indiceCanditado: fitness[indiceCanditado]})
        
        fitnessOrdenado = sorted(fitnessCandidatos.items(), key=itemgetter(1))
        paisSelecionados.append(populacao[fitnessOrdenado[0][0]])
        primeiroGanhador = fitnessOrdenado[0][0]
    return paisSelecionados


def funcao_dizimacao_corte(pop, escolaridade, referencial, listaDeAlimentos, listaDeCriacoes):
    fitnessCandidatos = funcao_fitness(pop, escolaridade, referencial, listaDeAlimentos, listaDeCriacoes)    
    fitnessOrdenado = sorted(fitnessCandidatos.items(), key=itemgetter(1))
    qtdRemocao = int(len(pop) * 0.4)
    remover = list()

    for cont in range(len(fitnessOrdenado) - 1, len(fitnessOrdenado) - qtdRemocao - 1, -1):
        remover.append(pop[fitnessOrdenado[cont][0]])

    for valor in remover:
        pop.remove(valor)

    return pop


def funcao_dizimacao_pais(pop):
    pais = list()

    pai1 = random.randint(0, len(pop) - 1)
    pais.append(pop[pai1])

    pai2 = pai1
    while pai2 == pai1:
        pai2 = random.randint(0, len(pop) - 1)

    pais.append(pop[pai2])

    return pais


def cruzamento(pais, taxa_cruzamento):
    filhos1_lista = list()
    filhos2_lista = list()
    filhos = list()

    if random.random() < taxa_cruzamento:
        for dia in range(0, len(pais[0])):
            filhoAux1 = dict()
            filhoAux2 = dict()
            for refeicao in pais[0][0].keys():
                tamanho = len(pais[0][0][refeicao])
                corte = random.randint(0, tamanho - 2) + 1
                filho1 = pais[0][dia][refeicao][0:corte] + pais[1][dia][refeicao][corte:tamanho]
                filho2 = pais[1][dia][refeicao][0:corte] + pais[0][dia][refeicao][corte:tamanho]

                filhoAux1.update({refeicao: filho1})
                filhoAux2.update({refeicao: filho2})
            filhos1_lista.append(filhoAux1)
            filhos2_lista.append(filhoAux2)
        filhos.append(filhos1_lista)
        filhos.append(filhos2_lista)
    else:
        filhos.append(pais[0])
        filhos.append(pais[1])

    return filhos

def listaTodosPratosPorCategoria(categoria, pratos):
    return [x for x in pratos if x.categoria == categoria]


def mutacao(filhos, taxa_mutacao, pratos):

    if random.random() < taxa_mutacao:
        for filho in filhos:
            dias = len(filho)
            dia_escolhido = random.randint(0, dias - 1)
            for refeicao in filho[dia_escolhido]:
                qtd_pratos = len(filho[dia_escolhido][refeicao])
                indice_mut = random.randint(0, qtd_pratos - 1)
                mutado = filho[dia_escolhido][refeicao][indice_mut]
                listaDePratos = listaTodosPratosPorCategoria(filho[dia_escolhido][refeicao][indice_mut].categoria, pratos)
                
                while mutado == filho[dia_escolhido][refeicao][indice_mut]:
                    mutado = random.choice(listaDePratos)

                filho[dia_escolhido][refeicao][indice_mut] = mutado

    return filhos
