import { useState } from 'react'
import { Plus, FileText, Send, CheckCircle, XCircle, Clock, AlertCircle } from 'lucide-react'
import { useInvoices, useSendToSifen } from '../hooks/useApi'
import InvoiceForm from '../components/InvoiceForm'

const statusConfig = {
  draft: { label: 'Borrador', icon: FileText, color: 'bg-gray-100 text-gray-700' },
  pending: { label: 'Pendiente', icon: Clock, color: 'bg-yellow-100 text-yellow-700' },
  sent: { label: 'Enviado', icon: Send, color: 'bg-blue-100 text-blue-700' },
  approved: { label: 'Aprobado', icon: CheckCircle, color: 'bg-green-100 text-green-700' },
  rejected: { label: 'Rechazado', icon: XCircle, color: 'bg-red-100 text-red-700' },
  cancelled: { label: 'Anulado', icon: AlertCircle, color: 'bg-gray-100 text-gray-700' },
}

export default function Invoices() {
  const [showForm, setShowForm] = useState(false)
  const { data: invoices, isLoading, refetch } = useInvoices()
  const sendToSifen = useSendToSifen()

  const handleSend = async (id: number) => {
    try {
      await sendToSifen.mutateAsync(id)
      refetch()
    } catch (error) {
      console.error('Error sending to SIFEN:', error)
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
    <div>
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Facturas</h1>
        <button 
          onClick={() => setShowForm(true)}
          className="flex items-center gap-2 bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors"
        >
          <Plus className="w-5 h-5" />
          Nueva Factura
        </button>
      </div>

      {isLoading ? (
        <div className="text-center py-8 text-gray-500">Cargando...</div>
      ) : invoices?.length > 0 ? (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <table className="w-full">
            <thead className="bg-gray-50 border-b">
              <tr>
                <th className="px-4 py-3 text-left text-sm font-medium text-gray-600">Número</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-gray-600">Receptor</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-gray-600">Fecha</th>
                <th className="px-4 py-3 text-right text-sm font-medium text-gray-600">Total</th>
                <th className="px-4 py-3 text-center text-sm font-medium text-gray-600">Estado</th>
                <th className="px-4 py-3 text-center text-sm font-medium text-gray-600">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {invoices.map((invoice: {
                id: number
                numero_completo: string
                receptor_nombre: string
                fecha_emision: string
                total: number
                status: keyof typeof statusConfig
                cdc: string
              }) => {
                const status = statusConfig[invoice.status] || statusConfig.draft
                const StatusIcon = status.icon
                
                return (
                  <tr key={invoice.id} className="hover:bg-gray-50">
                    <td className="px-4 py-3">
                      <div className="font-medium text-gray-900">{invoice.numero_completo}</div>
                      {invoice.cdc && (
                        <div className="text-xs text-gray-500 font-mono truncate max-w-[200px]">
                          CDC: {invoice.cdc}
                        </div>
                      )}
                    </td>
                    <td className="px-4 py-3 text-gray-600">{invoice.receptor_nombre}</td>
                    <td className="px-4 py-3 text-gray-600">
                      {new Date(invoice.fecha_emision).toLocaleDateString('es-PY')}
                    </td>
                    <td className="px-4 py-3 text-right font-medium text-gray-900">
                      {formatCurrency(invoice.total)}
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex justify-center">
                        <span className={`inline-flex items-center gap-1 px-2 py-1 text-xs rounded-full ${status.color}`}>
                          <StatusIcon className="w-3 h-3" />
                          {status.label}
                        </span>
                      </div>
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex justify-center gap-2">
                        {['draft', 'pending', 'rejected'].includes(invoice.status) && (
                          <button
                            onClick={() => handleSend(invoice.id)}
                            disabled={sendToSifen.isPending}
                            className="text-sm text-primary-600 hover:text-primary-700 font-medium"
                          >
                            Enviar a SIFEN
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200">
          <div className="p-8 text-center text-gray-500">
            <FileText className="w-12 h-12 mx-auto mb-4 text-gray-300" />
            <p>No hay facturas todavía.</p>
            <p className="text-sm mt-2">Crea tu primera factura electrónica.</p>
          </div>
        </div>
      )}

      {showForm && (
        <InvoiceForm 
          onClose={() => setShowForm(false)} 
          onSuccess={() => refetch()}
        />
      )}
    </div>
  )
}
