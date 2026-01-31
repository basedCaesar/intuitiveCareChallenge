WITH períodos AS (
    SELECT 
        MIN(ano * 10 + trimestre) as primeiro_p,
        MAX(ano * 10 + trimestre) as ultimo_p
    FROM despesas_consolidadas
),
primeiro_tri AS (
    SELECT cnpj, SUM(valor_despesas) as valor 
    FROM despesas_consolidadas, períodos
    WHERE (ano * 10 + trimestre) = períodos.primeiro_p
    GROUP BY cnpj
),
ultimo_tri AS (
    SELECT cnpj, SUM(valor_despesas) as valor 
    FROM despesas_consolidadas, períodos
    WHERE (ano * 10 + trimestre) = períodos.ultimo_p
    GROUP BY cnpj
)
SELECT 
    c.razao_social,
    p.valor as valor_inicial,
    u.valor as valor_final,
    ROUND(((u.valor - p.valor) / NULLIF(p.valor, 0)) * 100, 2) as crescimento_percentual
FROM primeiro_tri p
JOIN ultimo_tri u ON p.cnpj = u.cnpj
JOIN cadastro_operadoras c ON p.cnpj = c.cnpj
WHERE p.valor > 0
ORDER BY crescimento_percentual DESC
LIMIT 5;