import { defineStore } from 'pinia'
import axios from 'axios'

interface Operadora {
  cnpj: string
  razao_social: string
}

interface DetalheOperadora extends Operadora {
  registro_ans?: string
  modalidade?: string
  uf?: string
}

interface HistoricoDespesa {
  trimestre: string
  ano: number
  valor_despesas: number
}

interface DespesaResponse {
  trimestre: string
  ano: number
  valor_despesas: string | number
}

interface Stats {
  total_geral: number
  media_geral: number
  top_5: Array<{
    razao_social: string
    valor_despesas: number
  }>
}

export const useOperadoraStore = defineStore('operadoras', {
  state: () => ({
    items: [] as Operadora[],
    metadata: {
      total: 0,
      page: 1,
      limit: 10,
      total_pages: 0
    },
    searchQuery: '',
    
    stats: null as Stats | null,
    
    selectedOperadora: null as DetalheOperadora | null,
    historico: [] as HistoricoDespesa[],
    
    loading: false,
    error: null as string | null
  }),

  actions: {
    async fetchOperadoras(page = 1) {
      this.loading = true
      this.error = null
      try {
        const { data } = await axios.get('/api/operadoras', {
          params: {
            page,
            limit: this.metadata.limit,
            search: this.searchQuery || undefined
          }
        })
        this.items = data.data
        this.metadata = data.metadata
      } catch (err: unknown) {
        this.handleError(err)
      } finally {
        this.loading = false
      }
    },

    async fetchStats() {
      try {
        const { data } = await axios.get('/api/estatisticas')
        this.stats = data
      } catch (err: unknown) {
        console.error('Erro ao carregar gráficos:', err)
      }
    },

    async fetchDetalhes(cnpj: string) {
      this.loading = true
      try {
        const { data } = await axios.get(`/api/operadoras/${cnpj}`)
        this.selectedOperadora = data
      } catch (err: unknown) {
        this.handleError(err)
      } finally {
        this.loading = false
      }
    },

    async fetchHistorico(cnpj: string) {
      try {
        const { data } = await axios.get<DespesaResponse[]>(`/api/operadoras/${cnpj}/despesas`)
        
        this.historico = data.map((item) => ({
          trimestre: item.trimestre,
          ano: item.ano,
          valor_despesas: Number(item.valor_despesas) 
        }))
      } catch (err: unknown) {
        console.error('Erro ao carregar histórico:', err)
        this.historico = [] 
      }
    },

    setSearch(query: string) {
      this.searchQuery = query
      this.fetchOperadoras(1)
    },

    handleError(err: unknown) {
      if (axios.isAxiosError(err)) {
        this.error = err.response?.data?.detail || 'Erro na comunicação com a API'
      } else {
        this.error = 'Ocorreu um erro inesperado'
      }
    }
  }
})