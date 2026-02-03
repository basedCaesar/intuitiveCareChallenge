<script setup lang="ts">
import { onMounted } from 'vue'
import { useOperadoraStore } from '@/stores/operadoras'
import OperadoraTable from '@/components/OperadoraTable.vue'
import UfChart from '@/components/UFChart.vue'

const store = useOperadoraStore()

onMounted(() => {
  store.fetchStats()
})
</script>

<template>
  <main class="dashboard">
    <header class="header">
      <h1>Painel de Operadoras</h1>
      <div v-if="store.stats" class="stats-overview">
        <div class="stat-card">
          <h3>Total Geral de Despesas</h3>
          <p>R$ {{ store.stats.total_geral.toLocaleString('pt-BR', { minimumFractionDigits: 2 }) }}</p>
        </div>
        <div class="stat-card">
          <h3>Média Geral</h3>
          <p>R$ {{ store.stats.media_geral.toLocaleString('pt-BR', { minimumFractionDigits: 2 }) }}</p>
        </div>
      </div>
    </header>
    
    <div v-if="store.error" class="error-banner">
      {{ store.error }}
    </div>

    <section class="content-stack">
      <div class="chart-section">
        <h2>Distribuição de Despesas (Top 5)</h2>
        <div v-if="store.loading && !store.stats" class="loading-placeholder">
          Carregando dados do gráfico...
        </div>
        <UfChart v-else />
      </div>

      <div class="table-section">
        <h2>Listagem de Operadoras</h2>
        <OperadoraTable />
      </div>
    </section>
  </main>
</template>

<style scoped>
.dashboard {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
}

.stats-overview {
  display: flex;
  gap: 1.5rem;
}

.stat-card {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  border-left: 5px solid #42b883;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.stat-card h3 {
  margin: 0 0 0.5rem 0;
  font-size: 0.9rem;
  color: #666;
  text-transform: uppercase;
}

.stat-card p {
  margin: 0;
  font-size: 1.4rem;
  font-weight: bold;
  color: #2c3e50;
}

.content-stack {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.table-section, .chart-section {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

.error-banner {
  background: #fee2e2;
  color: #dc2626;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
}

.loading-placeholder {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f9f9f9;
  border-radius: 8px;
  color: #999;
}

h2 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  font-size: 1.2rem;
  color: #444;
}

@media (max-width: 768px) {
  .header {
    flex-direction: column;
    gap: 1.5rem;
  }
}
</style>