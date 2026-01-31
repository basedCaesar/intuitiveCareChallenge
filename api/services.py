from fastapi import HTTPException
from sqlalchemy.orm import Session
import repositories
from decimal import Decimal, ROUND_HALF_UP

def list_operadoras_service(db: Session, page: int, limit: int, search: str):
    try:
        skip = (page - 1) * limit
        data, total = repositories.get_operadoras(db, skip, limit, search)
        total_pages = (total + limit - 1) // limit if total > 0 else 0
        return {
            "data": data,
            "metadata": {"total": total, "page": page, "limit": limit, "total_pages": total_pages}
        }
    except Exception as e:
        print(f"ERRO LISTAGEM: {e}")
        raise HTTPException(status_code=500, detail="Erro ao listar operadoras")

def get_operadora_details_service(db: Session, cnpj: str):
    operadora = repositories.get_operadora_by_cnpj(db, cnpj)
    if not operadora:
        raise HTTPException(status_code=404, detail="Operadora não encontrada")
    return operadora

def get_operadora_history_service(db: Session, cnpj: str):
    get_operadora_details_service(db, cnpj)
    return repositories.get_despesas_by_cnpj(db, cnpj)

def get_estatisticas_service(db: Session):
    try:
        agregados = repositories.get_all_agregados(db)
        
        if not agregados:
            return {"total_geral": Decimal("0.00"), "media_geral": Decimal("0.00"), "top_5": []}

        dados_lista = []
        for row in agregados:
            valor = row.valor_total if row.valor_total is not None else Decimal(0)
            qtd = row.qtd_trimestres if row.qtd_trimestres and row.qtd_trimestres > 0 else 1
            

            media_calc = valor / qtd

            dados_lista.append({
                "cnpj": row.cnpj,
                "razao_social": row.razao_social,
                "valor_despesas": Decimal(str(valor)),
                "media_trimestral": Decimal(str(media_calc)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            })

        if not dados_lista:
             return {"total_geral": Decimal("0.00"), "media_geral": Decimal("0.00"), "top_5": []}

        total_geral = sum(d["valor_despesas"] for d in dados_lista)
        media_geral = total_geral / len(dados_lista)
        top_5 = sorted(dados_lista, key=lambda x: x["valor_despesas"], reverse=True)[:5]
        
        return {
            "total_geral": total_geral.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            "media_geral": media_geral.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            "top_5": top_5
        }
    except Exception as e:
        print(f"LOG_ERRO_ESTATISTICAS: {e}")
        raise HTTPException(status_code=500, detail=f"Erro no servidor: {str(e)}")