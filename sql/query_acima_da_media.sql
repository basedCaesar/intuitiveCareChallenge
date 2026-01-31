WITH media_global AS (
    SELECT AVG(valor_despesas) as valor_medio FROM despesas_agregadas
)
SELECT 
    razao_social, 
    registro_ans,
    COUNT(*) as trimestres_acima_da_media
FROM despesas_agregadas, media_global
WHERE valor_despesas > media_global.valor_medio
GROUP BY razao_social, registro_ans
HAVING COUNT(*) >= 2
ORDER BY trimestres_acima_da_media DESC;