import { Plus } from 'lucide-react'

export default function Invoices() {
  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Facturas</h1>
        <button className="flex items-center gap-2 bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors">
          <Plus className="w-5 h-5" />
          Nueva Factura
        </button>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-200">
        <div className="p-8 text-center text-gray-500">
          <p>No hay facturas todavía.</p>
          <p className="text-sm mt-2">Crea tu primera factura electrónica.</p>
        </div>
      </div>
    </div>
  )
}
