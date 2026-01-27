import { FileText, CheckCircle, XCircle, Clock, Building2, TrendingUp } from 'lucide-react'
import { useInvoices, useCompanies, useSifenStatus } from '../hooks/useApi'

export default function Dashboard() {
  const { data: invoices } = useInvoices()
  const { data: companies } = useCompanies()
  const { data: sifenStatus } = useSifenStatus()

  // Calculate stats
  const stats = {
    total: invoices?.length || 0,
    approved: invoices?.filter((i: { status: string }) => i.status === 'approved').length || 0,
    pending: invoices?.filter((i: { status: string }) => ['draft', 'pending'].includes(i.status)).length || 0,
    rejected: invoices?.filter((i: { status: string }) => i.status === 'rejected').length || 0,
  }

  const totalAmount = invoices?.reduce((sum: number, i: { total: number }) => sum + i.total, 0) || 0

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('es-PY', {
      style: 'currency',
      currency: 'PYG',
      minimumFractionDigits: 0
    }).format(value)
  }

  const statCards = [
    { name: 'Total Facturas', value: stats.total.toString(), icon: FileText, color: 'bg-blue-500' },
    { name: 'Aprobadas', value: stats.approved.toString(), icon: CheckCircle, color: 'bg-green-500' },
    { name: 'Pendientes', value: stats.pending.toString(), icon: Clock, color: 'bg-yellow-500' },
    { name: 'Rechazadas', value: stats.rejected.toString(), icon: XCircle, color: 'bg-red-500' },
  ]

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-8">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((stat) => (
          <div
            key={stat.name}
            className="bg-white rounded-xl shadow-sm border border-gray-200 p-6"
          >
            <div className="flex items-center gap-4">
              <div className={`${stat.color} p-3 rounded-lg`}>
                <stat.icon className="w-6 h-6 text-white" />
              </div>
              <div>
                <p className="text-sm text-gray-500">{stat.name}</p>
                <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
        {/* Quick Stats */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-primary-600" />
            Resumen
          </h2>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Empresas registradas</span>
              <span className="font-semibold">{companies?.length || 0}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Total facturado</span>
              <span className="font-semibold text-green-600">{formatCurrency(totalAmount)}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Tasa de aprobación</span>
              <span className="font-semibold">
                {stats.total > 0 ? Math.round((stats.approved / stats.total) * 100) : 0}%
              </span>
            </div>
          </div>
        </div>

        {/* SIFEN Status */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <Building2 className="w-5 h-5 text-primary-600" />
            Estado SIFEN
          </h2>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Ambiente</span>
              <span className={`px-2 py-1 text-xs rounded-full ${
                sifenStatus?.environment === 'production' 
                  ? 'bg-green-100 text-green-700' 
                  : 'bg-yellow-100 text-yellow-700'
              }`}>
                {sifenStatus?.environment === 'production' ? 'Producción' : 'Test'}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Certificado</span>
              <span className={`px-2 py-1 text-xs rounded-full ${
                sifenStatus?.certificate_configured
                  ? 'bg-green-100 text-green-700'
                  : 'bg-red-100 text-red-700'
              }`}>
                {sifenStatus?.certificate_configured ? 'Configurado' : 'No configurado'}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Estado</span>
              <span className={`px-2 py-1 text-xs rounded-full ${
                sifenStatus?.status === 'configured'
                  ? 'bg-green-100 text-green-700'
                  : 'bg-yellow-100 text-yellow-700'
              }`}>
                {sifenStatus?.status === 'configured' ? 'Listo' : 'Pendiente'}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-6 bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          🇵🇾 ERP Paraguay - Sistema de Facturación Electrónica
        </h2>
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <p className="font-medium text-gray-700 mb-2">Backend</p>
            <ul className="space-y-1 text-gray-500">
              <li>✅ Django 5.0 + REST API</li>
              <li>✅ Generador CDC (44 chars)</li>
              <li>✅ Constructor XML SIFEN v150</li>
              <li>✅ Cliente SOAP</li>
              <li>✅ Catálogos DNIT</li>
            </ul>
          </div>
          <div>
            <p className="font-medium text-gray-700 mb-2">Frontend</p>
            <ul className="space-y-1 text-gray-500">
              <li>✅ React 18 + TypeScript</li>
              <li>✅ Formularios de empresa</li>
              <li>✅ Formularios de factura</li>
              <li>✅ Dashboard con estadísticas</li>
              <li>✅ Integración API</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}
