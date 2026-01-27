import { useState } from 'react'
import { useForm, useFieldArray } from 'react-hook-form'
import { X, Plus, Trash2 } from 'lucide-react'
import { useCompanies, useCreateInvoice } from '../hooks/useApi'

interface InvoiceItem {
  codigo: string
  descripcion: string
  cantidad: number
  precio_unitario: number
  tasa_iva: number
}

interface InvoiceFormData {
  company: number
  establishment: number
  document_type: string
  receptor_ruc: string
  receptor_nombre: string
  receptor_direccion: string
  receptor_email: string
  moneda: string
  items: InvoiceItem[]
}

interface Props {
  onClose: () => void
  onSuccess: () => void
}

export default function InvoiceForm({ onClose, onSuccess }: Props) {
  const { register, handleSubmit, control, watch, formState: { errors } } = useForm<InvoiceFormData>({
    defaultValues: {
      document_type: '1',
      moneda: 'PYG',
      items: [{ codigo: '', descripcion: '', cantidad: 1, precio_unitario: 0, tasa_iva: 10 }]
    }
  })
  
  const { fields, append, remove } = useFieldArray({ control, name: 'items' })
  const { data: companies } = useCompanies()
  const createInvoice = useCreateInvoice()
  
  const selectedCompanyId = watch('company')
  const selectedCompany = companies?.find((c: { id: number }) => c.id === Number(selectedCompanyId))
  const items = watch('items')

  // Calculate totals
  const calculateTotals = () => {
    let total10 = 0, total5 = 0, exento = 0
    
    items?.forEach(item => {
      const subtotal = (item.cantidad || 0) * (item.precio_unitario || 0)
      if (item.tasa_iva === 10) total10 += subtotal
      else if (item.tasa_iva === 5) total5 += subtotal
      else exento += subtotal
    })
    
    return {
      subtotal_gravado_10: total10,
      subtotal_gravado_5: total5,
      subtotal_exento: exento,
      total_iva_10: total10 - (total10 / 1.1),
      total_iva_5: total5 - (total5 / 1.05),
      total: total10 + total5 + exento
    }
  }

  const totals = calculateTotals()

  const onSubmit = async (data: InvoiceFormData) => {
    try {
      // Get next invoice number (simplified - should come from backend)
      const numero = Math.floor(Math.random() * 1000000) + 1
      
      const invoiceData = {
        ...data,
        numero,
        timbrado: selectedCompany?.timbrado || '00000000',
        fecha_emision: new Date().toISOString(),
        ...totals,
        items: data.items.map(item => ({
          ...item,
          subtotal: item.cantidad * item.precio_unitario,
          iva: item.tasa_iva > 0 
            ? (item.cantidad * item.precio_unitario) - ((item.cantidad * item.precio_unitario) / (1 + item.tasa_iva / 100))
            : 0,
          total: item.cantidad * item.precio_unitario,
        }))
      }
      
      await createInvoice.mutateAsync(invoiceData)
      onSuccess()
      onClose()
    } catch (error) {
      console.error('Error creating invoice:', error)
    }
  }

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('es-PY', {
      style: 'currency',
      currency: 'PYG',
      minimumFractionDigits: 0
    }).format(value)
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl shadow-xl w-full max-w-4xl max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center p-6 border-b sticky top-0 bg-white">
          <h2 className="text-xl font-semibold">Nueva Factura Electrónica</h2>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
            <X className="w-6 h-6" />
          </button>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="p-6 space-y-6">
          {/* Emisor */}
          <div className="bg-gray-50 p-4 rounded-lg">
            <h3 className="font-medium text-gray-900 mb-3">Datos del Emisor</h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Empresa *
                </label>
                <select
                  {...register('company', { required: true })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                >
                  <option value="">Seleccionar empresa...</option>
                  {companies?.map((c: { id: number; razon_social: string; ruc: string }) => (
                    <option key={c.id} value={c.id}>
                      {c.razon_social} ({c.ruc})
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Establecimiento *
                </label>
                <select
                  {...register('establishment', { required: true })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                >
                  <option value="">Seleccionar...</option>
                  {selectedCompany?.establishments?.map((e: { id: number; codigo_establecimiento: string; codigo_punto: string }) => (
                    <option key={e.id} value={e.id}>
                      {e.codigo_establecimiento}-{e.codigo_punto}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {/* Receptor */}
          <div className="bg-gray-50 p-4 rounded-lg">
            <h3 className="font-medium text-gray-900 mb-3">Datos del Receptor</h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  RUC / CI
                </label>
                <input
                  {...register('receptor_ruc')}
                  placeholder="12345678-9"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Nombre / Razón Social *
                </label>
                <input
                  {...register('receptor_nombre', { required: true })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Dirección
                </label>
                <input
                  {...register('receptor_direccion')}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Email
                </label>
                <input
                  {...register('receptor_email')}
                  type="email"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
              </div>
            </div>
          </div>

          {/* Items */}
          <div>
            <div className="flex justify-between items-center mb-3">
              <h3 className="font-medium text-gray-900">Ítems</h3>
              <button
                type="button"
                onClick={() => append({ codigo: '', descripcion: '', cantidad: 1, precio_unitario: 0, tasa_iva: 10 })}
                className="flex items-center gap-1 text-sm text-primary-600 hover:text-primary-700"
              >
                <Plus className="w-4 h-4" /> Agregar ítem
              </button>
            </div>

            <div className="space-y-3">
              {fields.map((field, index) => (
                <div key={field.id} className="bg-gray-50 p-3 rounded-lg">
                  <div className="grid grid-cols-12 gap-2">
                    <div className="col-span-2">
                      <input
                        {...register(`items.${index}.codigo`)}
                        placeholder="Código"
                        className="w-full px-2 py-1.5 text-sm border border-gray-300 rounded"
                      />
                    </div>
                    <div className="col-span-4">
                      <input
                        {...register(`items.${index}.descripcion`, { required: true })}
                        placeholder="Descripción"
                        className="w-full px-2 py-1.5 text-sm border border-gray-300 rounded"
                      />
                    </div>
                    <div className="col-span-1">
                      <input
                        {...register(`items.${index}.cantidad`, { valueAsNumber: true })}
                        type="number"
                        min="1"
                        step="0.01"
                        placeholder="Cant."
                        className="w-full px-2 py-1.5 text-sm border border-gray-300 rounded"
                      />
                    </div>
                    <div className="col-span-2">
                      <input
                        {...register(`items.${index}.precio_unitario`, { valueAsNumber: true })}
                        type="number"
                        min="0"
                        placeholder="Precio"
                        className="w-full px-2 py-1.5 text-sm border border-gray-300 rounded"
                      />
                    </div>
                    <div className="col-span-2">
                      <select
                        {...register(`items.${index}.tasa_iva`, { valueAsNumber: true })}
                        className="w-full px-2 py-1.5 text-sm border border-gray-300 rounded"
                      >
                        <option value={10}>IVA 10%</option>
                        <option value={5}>IVA 5%</option>
                        <option value={0}>Exento</option>
                      </select>
                    </div>
                    <div className="col-span-1 flex items-center justify-center">
                      {fields.length > 1 && (
                        <button
                          type="button"
                          onClick={() => remove(index)}
                          className="text-red-500 hover:text-red-700"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Totals */}
          <div className="bg-gray-50 p-4 rounded-lg">
            <div className="grid grid-cols-3 gap-4 text-sm">
              <div>
                <span className="text-gray-600">Gravado 10%:</span>
                <span className="ml-2 font-medium">{formatCurrency(totals.subtotal_gravado_10)}</span>
              </div>
              <div>
                <span className="text-gray-600">Gravado 5%:</span>
                <span className="ml-2 font-medium">{formatCurrency(totals.subtotal_gravado_5)}</span>
              </div>
              <div>
                <span className="text-gray-600">Exento:</span>
                <span className="ml-2 font-medium">{formatCurrency(totals.subtotal_exento)}</span>
              </div>
            </div>
            <div className="mt-3 pt-3 border-t flex justify-end">
              <div className="text-right">
                <span className="text-gray-600">Total:</span>
                <span className="ml-2 text-xl font-bold text-gray-900">
                  {formatCurrency(totals.total)}
                </span>
              </div>
            </div>
          </div>

          <div className="flex justify-end gap-3 pt-4 border-t">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={createInvoice.isPending}
              className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50"
            >
              {createInvoice.isPending ? 'Creando...' : 'Crear Factura'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
