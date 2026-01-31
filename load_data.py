import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

def run_ingestion():
    db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    engine = create_engine(db_url)

    
    df_cad = pd.read_csv('output/dados_cadastrais/Relatorio_cadop.csv', sep=';', encoding='utf-8', dtype={'CNPJ': str})
    df_cad.columns = [c.lower().strip() for c in df_cad.columns]
    df_cad = df_cad.rename(columns={
        'registro_operadora': 'registro_ans',
        'regiao_de_comercializacao': 'regiao_comercializacao'
    })
    df_cad.to_sql('cadastro_operadoras', engine, if_exists='append', index=False)

    
    df_desp = pd.read_csv('output/consolidado/consolidado_despesas.csv', sep=';', encoding='utf-8', dtype={'CNPJ': str})
    
    
    df_desp['data_inconsistente'] = df_desp['data_inconsistente'].astype(bool)
    df_desp['valor_suspeito'] = df_desp['valor_suspeito'].astype(bool)
    
    df_desp = df_desp.rename(columns={
        'CNPJ': 'cnpj',
        'RazaoSocial': 'razao_social',
        'Trimestre': 'trimestre',
        'Ano': 'ano',
        'ValorDespesas': 'valor_despesas'
    })
    df_desp.to_sql('despesas_consolidadas', engine, if_exists='append', index=False)

   
    df_agr = pd.read_csv('output/agregado/despesas_agregadas.csv', sep=';', encoding='utf-8', dtype={'CNPJ': str})
    df_agr = df_agr.rename(columns={
        'CNPJ': 'cnpj',
        'RazaoSocial': 'razao_social',
        'Modalidade': 'modalidade',
        'UF': 'uf',
        'Trimestre': 'trimestre',
        'Ano': 'ano',
        'RegistroANS': 'registro_ans',
        'ValorDespesas': 'valor_despesas',
        'MediaTrimestral': 'media_trimestral',
        'DesvioPadraoTrimestral': 'desvio_padrao_trimestral'
    })
    df_agr.to_sql('despesas_agregadas', engine, if_exists='append', index=False)

if __name__ == "__main__":
    run_ingestion()