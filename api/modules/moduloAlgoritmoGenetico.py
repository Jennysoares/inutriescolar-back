from api.modules.moduloMenu import gerarMenu
from sqlalchemy.orm import Session
import random
from api.model.querysBusca import buscarReferencial, buscarCriacao, buscarComidaPorGrupoDeIds
from operator import itemgetter
from api.modules.moduloPrato import retornaListaDePratosPorCategoriaRefeicao


def gerar_populacao(tam_pop, qtdDias, db: Session):
    populacao = []
    

    for i in range(tam_pop):
        cardapioSemanal = []
        for j in range(qtdDias):
            individuo = gerarMenu(db=db)
            cardapioSemanal.append(individuo)
        populacao.append(cardapioSemanal)

    return populacao

def funcao_fitness(populacao, tipo, escolaridade, db: Session):
    fitness_valores = dict()
    if tipo == 1:
        for i in range(0, len(populacao)):
            fitness = funcao_objetivo(populacao[i], escolaridade, db)
            fitness_valores[i] = fitness
    else:
        for i in range(0, len(populacao)):
            fitness = funcao_objetivo(populacao[i], escolaridade, db)
            fitness_valores[fitness] = i

    return fitness_valores


def funcao_objetivo(cardapio, escolaridade, db: Session):    
    referencial = buscarReferencial(db, escolaridade)[0]
    f1 = calcularErroNutri(cardapio, escolaridade, referencial, db)
    f2 = calcularCusto(cardapio,  referencial)

    aptidao = (0.6 * f1) + (0.4 * f2)
    aptidao = round(aptidao, 3)

    return aptidao


def calcularErroNutri(cardapio, escolaridadeId, referencial, db: Session):
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
                criacao = buscarCriacao(db, pratos.id)
                ids = [element.id_alimento for element in criacao]
                alimentosDoPrato = buscarComidaPorGrupoDeIds(db, ids)
                for ingrediente in criacao:
                    alimento = next(x for x in alimentosDoPrato if x.id == ingrediente.id_alimento )
                    for nutriente in alimento.__dict__ :
                        if nutriente in nutriCardapio.keys():
                            valorPrato = 0
                            if escolaridadeId == 1:
                                valorPrato = alimento.__dict__[nutriente] * ingrediente.qtdEnsinoCreche
                            elif escolaridadeId == 2:
                                valorPrato = alimento.__dict__[nutriente] * ingrediente.qtdEnsinoFun1
                            elif escolaridadeId == 3:
                                valorPrato = alimento.__dict__[nutriente] * ingrediente.qtdEnsinoFun2
                            elif escolaridadeId == 4:
                                valorPrato = alimento.__dict__[nutriente] * ingrediente.qtdEnsinoMedio

                            valor = nutriCardapio[nutriente] + valorPrato
                            nutriCardapio[nutriente] = valor

    # Restrição das cores

    coreslist = list()
    for dia in cardapio:
        for refeicao in dia:
            cores = dict(Amarelo=0, Vermelho=0, Verde=0, Marrom=0, Branco=0, Laranja=0)
            for pratos in dia[refeicao]:
                if pratos.categoria in ["Entrada", "Guarnição", "Sobremesa", "Bebidas"]:
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

    # Restrição Consistencia

    liqpas = 0
    for dia in cardapio:
        for refeicao in dia:
            for pratos in dia[refeicao]:
                if pratos.categoria in ["Acomp Feijão", "Guarnição", "Principal"]:
                    if pratos.consistencia == 'Liquída' or pratos.consistencia == 'Pastosa':
                        liqpas += 1

    restricaoConsistencia = 0
    if liqpas > 1:
        restricaoConsistencia = liqpas

    # Restrição Variedade

    restricaoRepeticao = 0
    for dia in cardapio:
        for pratoAlmoco in dia['Almoço']:
            if pratoAlmoco.categoria in ["Entrada","Guarnição", "Principal", "Sobremesa", "Bebidas"]:
                if pratoAlmoco in dia['Jantar']:
                    restricaoRepeticao += 1

        for pratosLanche in dia['Lanche']:
            if pratoAlmoco.categoria in ["Fruta","Bebidas", "Pão/Cereal"]:
                if pratosLanche in dia['Desjejum']:
                    restricaoRepeticao += 1

    indice = 0
    listIndRepet = list()
    for dia in cardapio:
        for diaComparacao in range(0, len(cardapio)):
            if indice != diaComparacao:
                for pratoAlmoco in dia['Almoço']:
                    if pratoAlmoco.categoria in ["Entrada","Guarnição", "Principal"]:
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

    print(referencial.custoAluno)
    if custoCardapio > referencial.custoAluno:
        w = 1

    penalidade = w * referencial.custoAluno

    return custoCardapio + penalidade

def funcao_roleta(pop, escolaridade, db: Session):
    fitnessCandidatos = funcao_fitness(pop, 1, escolaridade, db)    
    fitnessTotal = round(sum(fitnessCandidatos.values()))
    roleta = list()
    for indiceCandidato in fitnessCandidatos.keys():
        proporcao = round(fitnessCandidatos[indiceCandidato]) * 100 / fitnessTotal
        for j in range(0, round(proporcao)):
            roleta.append(indiceCandidato)

    pais = list()

    pai1 = random.randint(0, len(roleta) - 1)
    pais.append(pop[roleta[pai1]])

    pai2 = pai1
    while pai2 == pai1:
        pai2 = random.randint(0, len(roleta) - 1)

    pais.append(pop[roleta[pai2]])

    return pais     

    
def funcao_torneio(pop, escolaridade, db: Session):
    populacao = list(pop[:])
    tamanhoPopulacao = len(populacao)
    qtdPopulacaoTorneio = int(tamanhoPopulacao * 0.6)
    paisSelecionados = list()
    while len(paisSelecionados) != 2:
        indicesCandidatosSelecionados = list()
        cromossomosCanditados = list()

        while len(cromossomosCanditados) != qtdPopulacaoTorneio:
            indiceCanditado = random.randint(0, len(populacao) - 1)
            if indiceCanditado not in indicesCandidatosSelecionados:
                indicesCandidatosSelecionados.append(indiceCanditado)
                cromossomosCanditados.append(populacao[indiceCanditado])

        fitnessCandidatos = funcao_fitness(cromossomosCanditados, 1, escolaridade, db)    
        fitnessOrdenado = sorted(fitnessCandidatos.items(), key=itemgetter(1))
        paisSelecionados.append(cromossomosCanditados[fitnessOrdenado[0][0]])
        indiceCandidatoGanhador = populacao.index(cromossomosCanditados[fitnessOrdenado[0][0]])
        del populacao[indiceCandidatoGanhador]
    return paisSelecionados


def funcao_dizimacao_corte(pop, escolaridade, db: Session):
    fitnessCandidatos = funcao_fitness(pop, 1, escolaridade, db)    
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

def listaTodosPratosPorCategoria(categoria, refeicao, db: Session):
    return retornaListaDePratosPorCategoriaRefeicao(refeicao, categoria, db)


def mutacao(filhos, taxa_mutacao,  db: Session):
    if random.random() < taxa_mutacao:
        for filho in filhos:
            dias = len(filho)
            dia_escolhido = random.randint(0, dias - 1)
            for refeicao in filho[dia_escolhido]:
                qtd_pratos = len(filho[dia_escolhido][refeicao])
                indice_mut = random.randint(0, qtd_pratos - 1)
                mutado = filho[dia_escolhido][refeicao][indice_mut]

                while mutado == filho[dia_escolhido][refeicao][indice_mut]:
                    mutado = random.choice(listaTodosPratosPorCategoria(filho[dia_escolhido][refeicao][indice_mut].categoria, refeicao, db))

                filho[dia_escolhido][refeicao][indice_mut] = mutado

    return filhos
