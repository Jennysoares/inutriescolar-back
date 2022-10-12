from typing import List, Optional

from pydantic import BaseModel


class AlimentoBase(BaseModel):
    id: int
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
    


class AlimentoCreate(AlimentoBase):
    pass


class Alimento(BaseModel):
    id: int

    class Config:
        orm_mode = True


class PratoBase(BaseModel):
    id: int
    nome: str
    categoria: str
    cor: str
    consistencia: str
    valor: float


class PratoCreate(PratoBase):
    pass


class Prato(BaseModel):
    id: int

    class Config:
        orm_mode = True


class CriacaoBase(BaseModel):
    id_alimento: int
    id_prato: int
    qtdEnsinoCreche: int
    qtdEnsinoFun1: int
    qtdEnsinoFun2: int
    qtdEnsinoMedio: int


class CriacaoCreate(CriacaoBase):
    pass


class Criacao(BaseModel):
    id: int
    id_alimento: int
    id_prato: int

    class Config:
        orm_mode = True


class ReferencialNutrientesBase(BaseModel):
    id: int
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


class ReferencialCreate(ReferencialNutrientesBase):
    pass


class ReferencialNutrientes(BaseModel):
    id: int

    class Config:
        orm_mode = True