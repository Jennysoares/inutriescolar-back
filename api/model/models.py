from sqlalchemy import  Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from .database import Base


class Prato(Base):
    __tablename__ = "pratos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(1000))
    categoria=Column(String(500))
    cor = Column(String(255))
    consistencia = Column(String(255))
    valor = Column(Float)
    
    criacao = relationship("Criacao", back_populates="pratos")


class Alimento(Base):
    __tablename__ = "alimentos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(1000))
    energia = Column(Integer)
    proteinas = Column(Float)
    carboidratos = Column(Float)
    lipideos = Column(Float)
    fibras = Column(Float)
    calcio = Column(Integer)
    ferro = Column(Float)
    zinco = Column(Float)
    magnesio = Column(Integer)
    grupo = Column(String(500))
    
    criacao = relationship("Criacao", back_populates="alimentos")
  
class Criacao(Base):
    __tablename__ = "criacao"

    id = Column(Integer, primary_key=True, index=True)
    id_alimento = Column(Integer, ForeignKey("alimentos.id"))
    id_prato = Column(Integer, ForeignKey("pratos.id"))
    qtdEnsinoCreche= Column(Integer)
    qtdEnsinoFun1 = Column(Integer)
    qtdEnsinoFun2 = Column(Integer)
    qtdEnsinoMedio= Column(Integer)
    

    pratos = relationship("Prato", back_populates="criacao")
    alimentos = relationship("Alimento", back_populates="criacao")


class ReferencialNutrientes(Base):
    __tablename__ = "referencialNutrientes"

    id = Column(Integer, primary_key=True, index=True)
    escolaridade = Column(Integer)
    energia = Column(Integer)
    proteinas = Column(Float)
    carboidratos = Column(Float)
    lipideos = Column(Float)
    fibras = Column(Float)
    calcio = Column(Integer)
    ferro = Column(Float)
    zinco = Column(Float)
    magnesio = Column(Integer)
    custoAluno = Column(Float)
