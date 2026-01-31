CREATE TABLE IF NOT EXISTS cadastro_operadoras (
    cnpj VARCHAR(20) PRIMARY KEY,
    registro_ans VARCHAR(20),
    razao_social TEXT,
    nome_fantasia TEXT,
    modalidade TEXT,
    logradouro TEXT,
    numero TEXT,
    complemento TEXT,
    bairro TEXT,
    cidade TEXT,
    uf CHARACTER(2),
    cep VARCHAR(10),
    ddd TEXT,
    telefone TEXT,
    fax TEXT,
    endereco_eletronico TEXT,
    representante TEXT,
    cargo_representante TEXT,
    regiao_comercializacao TEXT,
    data_registro_ans DATE
);

CREATE TABLE IF NOT EXISTS despesas_consolidadas (
    id SERIAL PRIMARY KEY,
    cnpj VARCHAR(20) REFERENCES cadastro_operadoras(cnpj),
    razao_social TEXT,
    trimestre INTEGER,
    ano INTEGER,
    valor_despesas NUMERIC(15,2),
    data_inconsistente BOOLEAN DEFAULT FALSE,
    valor_suspeito BOOLEAN DEFAULT FALSE,
    casos_suspeitos INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS despesas_agregadas (
    id SERIAL PRIMARY KEY,
    cnpj VARCHAR(20) REFERENCES cadastro_operadoras(cnpj),
    razao_social TEXT,
    modalidade TEXT,
    uf CHARACTER(2),
    trimestre INTEGER,
    ano INTEGER,
    registro_ans VARCHAR(20),
    valor_despesas NUMERIC(15,2),
    media_trimestral NUMERIC(15,2),
    desvio_padrao_trimestral NUMERIC(15,2)
);

CREATE INDEX IF NOT EXISTS idx_cnpj_despesas ON despesas_consolidadas(cnpj);
CREATE INDEX IF NOT EXISTS idx_cnpj_agregadas ON despesas_agregadas(cnpj);
CREATE INDEX IF NOT EXISTS idx_registro_ans ON cadastro_operadoras(registro_ans);