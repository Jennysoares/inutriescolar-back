from ast import Dict
from typing import List, Optional

from pydantic import BaseModel


class Alimento(BaseModel):
    nome: str
    energia: int
    proteinas: float
    carboidratos: float
    lipideos: float
    fibras: float
    calcio: int
    ferro: float
    zinco: float
    magnesio: int
    grupo: str
    

class Prato(BaseModel):
    nome: str
    categoria: str
    cor: str
    consistencia: str
    valor: float



class Criacao(BaseModel):
    id_alimento: int
    id_prato: int
    qtdEnsinoCreche: float
    qtdEnsinoFun1: float
    qtdEnsinoFun2: float
    qtdEnsinoMedio: float

class CriacaoList(BaseModel):
    data: List[Criacao]

class ReferencialNutrientes(BaseModel):
    escolaridade: int 
    energia: int
    proteinas: float
    carboidratos: float
    lipideos: float
    fibras: float
    calcio: int 
    ferro: float
    zinco: float
    magnesio: int 
    custoAluno: float