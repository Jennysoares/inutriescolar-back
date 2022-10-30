import csv
from api.model import models
from api.model.database import SessionLocal, engine


class Data:

    def __init__(self):
        pass

    def importarDados(self, db):

        with open('api/model/food_data_alter.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f, delimiter=';')

            for linha in reader:
                db_alimentos = models.Alimento(
                    nome=linha[1],
                    energia= float(linha[2]),
                    proteinas=float(linha[3]),
                    lipideos=float(linha[4]),
                    carboidratos=float(linha[5]),
                    fibras=float(linha[6]),
                    calcio=float(linha[7]),
                    magnesio=float(linha[8]),
                    ferro=float(linha[9]),
                    zinco=float(linha[10]),
                    grupo=linha[11]
                )

                db.add(db_alimentos)
                

        with open('api/model/tabelaPratos.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f, delimiter=';')
            for linha in reader:
                db_pratos = models.Prato(
                    nome=linha[1].lower().capitalize(),
                    categoria= linha[2],
                    cor=linha[3],
                    consistencia=linha[4],
                    valor=float(linha[5]),
                )
                
                db.add(db_pratos)


        with open('api/model/tabelaAlimentosPratos.csv', 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f, delimiter=';')
            for linha in reader:
                db_pratos_alimentos = models.Criacao(
                    id_alimento = linha[0],
                    id_prato = linha[1],
                    qtdEnsinoCreche= 0,
                    qtdEnsinoFun1= linha[2],
                    qtdEnsinoFun2= linha[3],
                    qtdEnsinoMedio= linha[4]
                )
                
                
                db.add(db_pratos_alimentos)

            db.commit()

        db.close()

data_alimentos = Data()
