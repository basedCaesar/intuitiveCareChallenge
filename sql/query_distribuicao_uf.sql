SELECT 
    uf, 
    SUM(valor_despesas) as despesa_total,
    ROUND(AVG(valor_despesas), 2) as media_por_operadora
FROM despesas_agregadas
GROUP BY uf
ORDER BY despesa_total DESC
LIMIT 5;