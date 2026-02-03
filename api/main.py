from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import services
import schemas

app = FastAPI(title="ANS API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/operadoras", response_model=schemas.PagedResponse)
def list_operadoras(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str = Query(None),
    db: Session = Depends(get_db)
):
    return services.list_operadoras_service(db, page, limit, search)

@app.get("/api/operadoras/{cnpj}", response_model=schemas.OperadoraDetalhe)
def get_operadora(cnpj: str, db: Session = Depends(get_db)):
    return services.get_operadora_details_service(db, cnpj)

@app.get("/api/operadoras/{cnpj}/despesas", response_model=List[schemas.DespesaSchema])
def get_despesas(cnpj: str, db: Session = Depends(get_db)):
    return services.get_operadora_history_service(db, cnpj)

@app.get("/api/estatisticas", response_model=schemas.EstatisticasResponse)
def get_stats(db: Session = Depends(get_db)):
    return services.get_estatisticas_service(db)