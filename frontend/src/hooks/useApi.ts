import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import api, { companiesApi, invoicesApi, sifenApi } from '../services/api'

// Companies hooks
export function useCompanies() {
  return useQuery({
    queryKey: ['companies'],
    queryFn: async () => {
      const { data } = await companiesApi.list()
      return data.results || data
    },
  })
}

export function useCompany(id: number) {
  return useQuery({
    queryKey: ['companies', id],
    queryFn: async () => {
      const { data } = await companiesApi.get(id)
      return data
    },
    enabled: !!id,
  })
}

export function useCreateCompany() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: companiesApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['companies'] })
    },
  })
}

// Invoices hooks
export function useInvoices() {
  return useQuery({
    queryKey: ['invoices'],
    queryFn: async () => {
      const { data } = await invoicesApi.list()
      return data.results || data
    },
  })
}

export function useInvoice(id: number) {
  return useQuery({
    queryKey: ['invoices', id],
    queryFn: async () => {
      const { data } = await invoicesApi.get(id)
      return data
    },
    enabled: !!id,
  })
}

export function useCreateInvoice() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: invoicesApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['invoices'] })
    },
  })
}

export function useSendToSifen() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: number) => invoicesApi.sendToSifen(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['invoices'] })
    },
  })
}

// SIFEN hooks
export function useSifenStatus() {
  return useQuery({
    queryKey: ['sifen', 'status'],
    queryFn: async () => {
      const { data } = await sifenApi.status()
      return data
    },
  })
}

// Catalogs hooks
export function useDepartamentos() {
  return useQuery({
    queryKey: ['catalogs', 'departamentos'],
    queryFn: async () => {
      const { data } = await api.get('/sifen/catalogs/departamentos/')
      return data
    },
  })
}

export function useActividades(search: string) {
  return useQuery({
    queryKey: ['catalogs', 'actividades', search],
    queryFn: async () => {
      if (search.length < 2) return []
      const { data } = await api.get(`/sifen/catalogs/actividades/search/?q=${search}`)
      return data
    },
    enabled: search.length >= 2,
  })
}

export function useMonedas() {
  return useQuery({
    queryKey: ['catalogs', 'monedas'],
    queryFn: async () => {
      const { data } = await api.get('/sifen/catalogs/monedas/')
      return data
    },
  })
}

export function useTasasIva() {
  return useQuery({
    queryKey: ['catalogs', 'iva'],
    queryFn: async () => {
      const { data } = await api.get('/sifen/catalogs/iva/')
      return data
    },
  })
}
