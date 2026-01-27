import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor for auth
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default api

// API endpoints
export const invoicesApi = {
  list: () => api.get('/invoicing/invoices/'),
  get: (id: number) => api.get(`/invoicing/invoices/${id}/`),
  create: (data: unknown) => api.post('/invoicing/invoices/', data),
  sendToSifen: (id: number) => api.post(`/invoicing/invoices/${id}/send_to_sifen/`),
}

export const companiesApi = {
  list: () => api.get('/companies/companies/'),
  get: (id: number) => api.get(`/companies/companies/${id}/`),
  create: (data: unknown) => api.post('/companies/companies/', data),
}

export const sifenApi = {
  status: () => api.get('/sifen/status/'),
  validateCdc: (cdc: string) => api.get(`/sifen/validate-cdc/${cdc}/`),
}
