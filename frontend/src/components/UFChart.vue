<script setup lang="ts">
import { computed } from 'vue'
import { useOperadoraStore } from '@/stores/operadoras'
import { Bar } from 'vue-chartjs'
import { 
  Chart as ChartJS, 
  Title, 
  Tooltip, 
  Legend, 
  BarElement, 
  CategoryScale, 
  LinearScale 
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const store = useOperadoraStore()

const chartData = computed(() => {
  if (!store.stats || !store.stats.top_5) return { labels: [], datasets: [] }

  return {
    labels: store.stats.top_5.map(item => item.razao_social),
    datasets: [
      {
        label: 'Despesas Totais (R$)',
        backgroundColor: '#42b883',
        data: store.stats.top_5.map(item => item.valor_despesas)
      }
    ]
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false
}
</script>

<template>
  <div class="chart-container">
    <Bar v-if="store.stats" :data="chartData" :options="chartOptions" />
    <div v-else class="loading-chart">Carregando dados do gráfico...</div>
  </div>
</template>

<style scoped>
.chart-container { height: 400px; position: relative; }
.loading-chart { display: flex; align-items: center; justify-content: center; height: 100%; border: 1px dashed #ccc; }
</style>