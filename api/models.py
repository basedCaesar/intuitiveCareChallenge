from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, Text, Date, Numeric
from sqlalchemy.orm import relationship
from database import Base

class Operadora(Base):
    __tablename__ = "cadastro_operadoras"

    cnpj = Column(String(20), primary_key=True)
    registro_ans = Column(String(20), index=True)
    razao_social = Column(Text)
    nome_fantasia = Column(Text)
    modalidade = Column(Text)
    logradouro = Column(Text)
    numero = Column(Text)
    complemento = Column(Text)
    bairro = Column(Text)
    cidade = Column(Text)
    uf = Column(String(2))
    cep = Column(String(10))
    ddd = Column(Text)
    telefone = Column(Text)
    fax = Column(Text)
    endereco_eletronico = Column(Text)
    representante = Column(Text)
    cargo_representante = Column(Text)
    regiao_comercializacao = Column(Text)
    data_registro_ans = Column(Date)

    despesas = relationship("Despesa", back_populates="operadora")

class Despesa(Base):
    __tablename__ = "despesas_consolidadas"

    id = Column(Integer, primary_key=True)
    cnpj = Column(String(20), ForeignKey("cadastro_operadoras.cnpj"), index=True)
    razao_social = Column(Text)
    trimestre = Column(Integer)
    ano = Column(Integer)
    valor_despesas = Column(Numeric(15, 2))
    data_inconsistente = Column(Boolean, default=False)
    valor_suspeito = Column(Boolean, default=False)
    casos_suspeitos = Column(Integer, default=0)

    operadora = relationship("Operadora", back_populates="despesas")

class DespesaAgregada(Base):
    __tablename__ = "despesas_agregadas"

    id = Column(Integer, primary_key=True)
    cnpj = Column(String(20), ForeignKey("cadastro_operadoras.cnpj"), index=True)
    razao_social = Column(Text)
    modalidade = Column(Text)
    uf = Column(String(2))
    trimestre = Column(Integer)
    ano = Column(Integer)
    registro_ans = Column(String(20))
    valor_despesas = Column(Numeric(15, 2))
    media_trimestral = Column(Numeric(15, 2))
    desvio_padrao_trimestral = Column(Numeric(15, 2))