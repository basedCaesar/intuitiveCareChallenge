import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def run_ingestion():
    db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    engine = create_engine(db_url)

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE cadastro_operadoras, despesas_consolidadas, despesas_agregadas CASCADE;"))

    df_cad = pd.read_csv('output/dados_cadastrais/Relatorio_cadop.csv', sep=';', encoding='utf-8', dtype={'CNPJ': str})
    df_cad.columns = [c.lower().strip() for c in df_cad.columns]
    df_cad['cnpj'] = df_cad['cnpj'].str.replace(r'\D', '', regex=True).str.strip()
    df_cad = df_cad.dropna(subset=['cnpj'])
    df_cad = df_cad.rename(columns={
        'registro_operadora': 'registro_ans',
        'regiao_de_comercializacao': 'regiao_comercializacao'
    })
    df_cad.to_sql('cadastro_operadoras', engine, if_exists='append', index=False)

    df_desp = pd.read_csv('output/consolidado/consolidado_despesas.csv', sep=';', encoding='utf-8', dtype={'CNPJ': str})
    
    df_desp = df_desp.dropna(subset=['CNPJ'])
    df_desp['CNPJ'] = df_desp['CNPJ'].str.replace(r'\D', '', regex=True).str.strip()

    df_desp['data_inconsistente'] = df_desp['data_inconsistente'].astype(int).astype(bool)
    df_desp['valor_suspeito'] = df_desp['valor_suspeito'].astype(int).astype(bool)
    
    df_desp = df_desp.rename(columns={
        'CNPJ': 'cnpj',
        'RazaoSocial': 'razao_social',
        'Trimestre': 'trimestre',
        'Ano': 'ano',
        'ValorDespesas': 'valor_despesas'
    })
    
    cols_consolidadas = ['cnpj', 'razao_social', 'trimestre', 'ano', 'valor_despesas', 'data_inconsistente', 'valor_suspeito']
    df_desp[cols_consolidadas].to_sql('despesas_consolidadas', engine, if_exists='append', index=False, method='multi', chunksize=1000)

    df_agr = pd.read_csv('output/agregado/despesas_agregadas.csv', sep=';', encoding='utf-8', dtype={'CNPJ': str})
    df_agr['CNPJ'] = df_agr['CNPJ'].str.replace(r'\D', '', regex=True).str.strip()
    df_agr = df_agr.dropna(subset=['CNPJ'])
    
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