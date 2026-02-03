<script setup lang="ts">
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import { useOperadoraStore } from '@/stores/operadoras'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  type TooltipItem
} from 'chart.js'


ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

const store = useOperadoraStore()


const chartData = computed(() => ({
  labels: store.historico.map(h => `${h.trimestre}º Trim / ${h.ano}`), // Melhorar o label
  datasets: [
    {
      label: 'Despesas Trimestrais',
      backgroundColor: 'rgba(66, 184, 131, 0.2)',
      borderColor: '#42b883',
      pointBackgroundColor: '#42b883',
      pointBorderColor: '#fff',
      data: store.historico.map(h => h.valor_despesas), 
      tension: 0.3,
      fill: true
    }
  ]
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top' as const
    },
    tooltip: {
      callbacks: {
        label: (context: TooltipItem<'line'>) => {
          const value = context.parsed.y ?? 0;
          return new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL'
          }).format(value)
        }
      }
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      grid: {
        color: '#f0f0f0'
      },
      ticks: {
        callback: (value: string | number) => {
          return Number(value).toLocaleString('pt-BR', {
            style: 'currency',
            currency: 'BRL',
            notation: 'compact'
          })
        }
      }
    },
    x: {
      grid: {
        display: false
      }
    }
  }
}
</script>

<template>
  <div class="chart-container">
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>

<style scoped>
.chart-container {
  position: relative;
  height: 100%;
  width: 100%;
  min-height: 350px;
}
</style>