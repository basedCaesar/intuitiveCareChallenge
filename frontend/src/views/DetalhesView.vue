<script setup lang="ts">
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useOperadoraStore } from '@/stores/operadoras'
import HistoryChart from '@/components/HistoryChart.vue'

const route = useRoute()
const store = useOperadoraStore()
const cnpj = route.params.cnpj as string

onMounted(async () => {
  await store.fetchDetalhes(cnpj)
  await store.fetchHistorico(cnpj)
})
</script>

<template>
  <div class="details-page">
    <router-link to="/" class="back-link">← Voltar ao Painel</router-link>
    
    <div v-if="store.loading" class="loading-state">
      <div class="spinner"></div>
      <p>Carregando informações da operadora...</p>
    </div>

    <div v-else-if="store.selectedOperadora" class="content-wrapper">
      <header class="details-header">
        <div class="title-group">
          <h1>{{ store.selectedOperadora.razao_social }}</h1>
          <div class="badges">
            <span class="badge-cnpj">CNPJ: {{ store.selectedOperadora.cnpj }}</span>
            <span v-if="store.selectedOperadora.registro_ans" class="badge-ans">
              ANS: {{ store.selectedOperadora.registro_ans }}
            </span>
          </div>
        </div>
      </header>

      <div class="details-grid">
        <section class="info-card">
          <h2>Dados Cadastrais</h2>
          <div class="info-item">
            <label>Modalidade</label>
            <span>{{ store.selectedOperadora.modalidade || 'Não informada' }}</span>
          </div>
          <div class="info-item">
            <label>UF</label>
            <span>{{ store.selectedOperadora.uf || 'N/A' }}</span>
          </div>
        </section>

        <section class="chart-card">
          <h2>Evolução Trimestral de Despesas</h2>
          <div v-if="store.historico && store.historico.length > 0" class="chart-container">
            <HistoryChart />
          </div>
          <div v-else class="empty-history">
            <p>Nenhum dado histórico encontrado para esta operadora.</p>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<style scoped>
.details-page { padding: 2rem; max-width: 1200px; margin: 0 auto; background-color: #f0f2f5; min-height: 100vh; }
.back-link { display: inline-block; margin-bottom: 1.5rem; color: #42b883; text-decoration: none; font-weight: 600; }
.content-wrapper { display: flex; flex-direction: column; gap: 2rem; }

.details-header { background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
.details-header h1 { margin: 0; font-size: 1.8rem; color: #2c3e50; }
.badges { margin-top: 1rem; display: flex; gap: 10px; }
.badge-cnpj, .badge-ans { background: #e8f5e9; color: #2e7d32; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: bold; }

.details-grid { display: grid; grid-template-columns: 350px 1fr; gap: 2rem; }
.info-card, .chart-card { background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }

h2 { font-size: 1.1rem; color: #666; margin-bottom: 1.5rem; border-bottom: 1px solid #eee; padding-bottom: 0.5rem; }

.info-item { margin-bottom: 1.5rem; }
.info-item label { display: block; font-size: 0.8rem; color: #999; text-transform: uppercase; margin-bottom: 0.2rem; }
.info-item span { font-size: 1.1rem; color: #333; font-weight: 500; }

.chart-container { height: 350px; }
.empty-history { text-align: center; padding: 4rem 0; color: #999; border: 2px dashed #eee; border-radius: 8px; }

@media (max-width: 900px) {
  .details-grid { grid-template-columns: 1fr; }
}
</style>