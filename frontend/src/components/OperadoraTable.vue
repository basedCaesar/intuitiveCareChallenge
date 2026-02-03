<script setup lang="ts">
import { onMounted, watch, ref } from 'vue'
import { useOperadoraStore } from '@/stores/operadoras'

const store = useOperadoraStore()
const searchTimeout = ref<ReturnType<typeof setTimeout> | null>(null)

onMounted(() => {
  store.fetchOperadoras()
})

watch(() => store.searchQuery, () => {
  if (searchTimeout.value) clearTimeout(searchTimeout.value)
  searchTimeout.value = setTimeout(() => {
    store.fetchOperadoras(1)
  }, 300)
})
</script>

<template>
  <div class="table-container">
    <div class="search-box">
      <input 
        v-model="store.searchQuery" 
        placeholder="Buscar por Razão Social ou CNPJ..."
        class="search-input"
      />
    </div>

    <div class="table-wrapper" :class="{ 'is-loading': store.loading }">
      <div v-if="store.loading" class="loading-overlay">
        <span>Carregando dados...</span>
      </div>

      <table class="styled-table">
        <thead>
          <tr>
            <th>CNPJ</th>
            <th>Razão Social</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="store.items.length === 0 && !store.loading">
            <td colspan="3" class="no-data">Nenhuma operadora encontrada.</td>
          </tr>
          <tr v-for="op in store.items" :key="op.cnpj">
            <td class="cnpj-cell">{{ op.cnpj }}</td>
            <td>{{ op.razao_social }}</td>
            <td>
              <router-link :to="`/detalhes/${op.cnpj}`" class="btn-detail">
                Ver Detalhes
              </router-link>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="pagination" v-if="store.metadata.total_pages > 1">
      <button 
        :disabled="store.metadata.page === 1 || store.loading" 
        @click="store.fetchOperadoras(store.metadata.page - 1)"
      >Anterior</button>
      
      <span class="page-info">
        Página <strong>{{ store.metadata.page }}</strong> de {{ store.metadata.total_pages }}
      </span>
      
      <button 
        :disabled="store.metadata.page === store.metadata.total_pages || store.loading" 
        @click="store.fetchOperadoras(store.metadata.page + 1)"
      >Próxima</button>
    </div>
  </div>
</template>

<style scoped>
.table-wrapper {
  position: relative;
  min-height: 450px;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.is-loading .styled-table {
  opacity: 0.5;
  pointer-events: none;
}

.search-input { width: 100%; padding: 12px; margin-bottom: 20px; border: 1px solid #ddd; border-radius: 4px; }
.styled-table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
.styled-table th, .styled-table td { padding: 12px; border-bottom: 1px solid #eee; text-align: left; }
.btn-detail { color: #42b883; text-decoration: none; font-weight: bold; }
.pagination { display: flex; justify-content: center; align-items: center; gap: 15px; margin-top: 20px; }
.no-data { text-align: center; padding: 40px; color: #999; }
</style>