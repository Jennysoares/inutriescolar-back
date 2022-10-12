import csv
from api.model import models
from api.model.database import SessionLocal, engine


class Data:

    def __init__(self):
        pass

    def importarDados(self, db):

        with open('api/model/food_data_alter.csv', 'r', encoding='utf-8-sig') as f:
            csv_reader = csv.DictReader(f)
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

            db.commit()

        db.close()

data_alimentos = Data()
