from sqlalchemy.orm import Session
from sqlalchemy import or_, func
import models

def get_operadoras(db: Session, skip: int, limit: int, search: str = None):
    query = db.query(models.Operadora)
    if search:
        query = query.filter(
            or_(
                models.Operadora.razao_social.ilike(f"%{search}%"),
                models.Operadora.cnpj.like(f"%{search}%")
            )
        )
    total = query.count()
    data = query.offset(skip).limit(limit).all()
    return data, total

def get_operadora_by_cnpj(db: Session, cnpj: str):
    return db.query(models.Operadora).filter(models.Operadora.cnpj == cnpj).first()

def get_despesas_by_cnpj(db: Session, cnpj: str):
    # Garante que o CNPJ consultado não tenha espaços ou símbolos
    cnpj_limpo = "".join(filter(str.isdigit, str(cnpj)))
    
    return db.query(
        models.Despesa.ano,
        models.Despesa.trimestre,
        func.sum(models.Despesa.valor_despesas).label("valor_despesas")
    ).filter(
        models.Despesa.cnpj == cnpj_limpo
    ).group_by(
        models.Despesa.ano, 
        models.Despesa.trimestre
    ).order_by(
        models.Despesa.ano.desc(), 
        models.Despesa.trimestre.desc()
    ).all()
def get_all_agregados(db: Session):

    return db.query(
        models.DespesaAgregada.cnpj,
        models.DespesaAgregada.razao_social,
        func.sum(models.DespesaAgregada.valor_despesas).label("valor_total"),
        func.count(models.DespesaAgregada.id).label("qtd_trimestres")
    ).group_by(
        models.DespesaAgregada.cnpj, 
        models.DespesaAgregada.razao_social
    ).all()