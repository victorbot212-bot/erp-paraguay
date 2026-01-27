// Company types
export interface Company {
  id: number
  ruc: string
  razon_social: string
  nombre_fantasia: string
  actividad_economica: string
  departamento: string
  distrito: string
  ciudad: string
  direccion: string
  telefono: string
  email: string
  timbrado: string
  is_active: boolean
  establishments: EstablishmentPoint[]
}

export interface EstablishmentPoint {
  id: number
  company: number
  codigo_establecimiento: string
  codigo_punto: string
  descripcion: string
  direccion: string
  is_active: boolean
}

// Invoice types
export type DocumentType = '1' | '2' | '3' | '4' | '5' | '6' | '7'
export type InvoiceStatus = 'draft' | 'pending' | 'sent' | 'approved' | 'rejected' | 'cancelled'

export interface InvoiceItem {
  id: number
  codigo: string
  descripcion: string
  unidad_medida: string
  cantidad: number
  precio_unitario: number
  descuento: number
  tasa_iva: 10 | 5 | 0
  subtotal: number
  iva: number
  total: number
}

export interface Invoice {
  id: number
  company: number
  establishment: number
  document_type: DocumentType
  numero: number
  numero_completo: string
  cdc: string
  timbrado: string
  receptor_ruc: string
  receptor_nombre: string
  receptor_direccion: string
  receptor_email: string
  fecha_emision: string
  moneda: string
  tipo_cambio: number
  subtotal_gravado_10: number
  subtotal_gravado_5: number
  subtotal_exento: number
  total_iva_10: number
  total_iva_5: number
  total: number
  status: InvoiceStatus
  items: InvoiceItem[]
}
