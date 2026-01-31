from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from decimal import Decimal
from datetime import date

class DespesaSchema(BaseModel):
    trimestre: int
    ano: int
    valor_despesas: Decimal
    model_config = ConfigDict(from_attributes=True)

class AgregadoSchema(BaseModel):
    cnpj: str
    razao_social: Optional[str] = None
    valor_despesas: Decimal
    media_trimestral: Optional[Decimal] = None 
    model_config = ConfigDict(from_attributes=True)

class EstatisticasResponse(BaseModel):
    total_geral: Decimal
    media_geral: Decimal
    top_5: List[AgregadoSchema]

class OperadoraLista(BaseModel):
    cnpj: str
    razao_social: str
    registro_ans: Optional[str] = None
    uf: Optional[str] = None
    modalidade: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class OperadoraDetalhe(OperadoraLista):
    nome_fantasia: Optional[str] = None
    logradouro: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    cep: Optional[str] = None
    ddd: Optional[str] = None
    telefone: Optional[str] = None
    fax: Optional[str] = None
    endereco_eletronico: Optional[str] = None
    representante: Optional[str] = None
    cargo_representante: Optional[str] = None
    regiao_comercializacao: Optional[str] = None
    data_registro_ans: Optional[date] = None

class Metadata(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int

class PagedResponse(BaseModel):
    data: List[OperadoraLista]
    metadata: Metadata