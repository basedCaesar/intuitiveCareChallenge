import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def run_analysis():
    db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    engine = create_engine(db_url)

    queries = {
        "Query 1: Crescimento Percentual (Top 5)": "sql/query_crescimento.sql",
        "Query 2: Distribuição por UF (Top 5)": "sql/query_distribuicao_uf.sql",
        "Query 3: Operadoras Acima da Média": "sql/query_acima_da_media.sql"
    }

    print("="*60)
    print("RELATÓRIO ANALÍTICO - DADOS ANS")
    print("="*60)

    for title, file_path in queries.items():
        print(f"\n>>> Executando {title}...")
        
        if not os.path.exists(file_path):
            print(f"Erro: Arquivo {file_path} não encontrado.")
            continue

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                sql_content = f.read()

            with engine.connect() as conn:
                df = pd.read_sql(text(sql_content), conn)

            if df.empty:
                print("Nenhum resultado encontrado para esta consulta.")
            else:
                print(df.to_string(index=False))
                
        except Exception as e:
            print(f"Erro ao processar a query: {e}")

    print("\n" + "="*60)
    print("Análise concluída com sucesso.")

if __name__ == "__main__":
    run_analysis()