import { FileText, CheckCircle, XCircle, Clock } from 'lucide-react'

const stats = [
  { name: 'Total Facturas', value: '0', icon: FileText, color: 'bg-blue-500' },
  { name: 'Aprobadas', value: '0', icon: CheckCircle, color: 'bg-green-500' },
  { name: 'Pendientes', value: '0', icon: Clock, color: 'bg-yellow-500' },
  { name: 'Rechazadas', value: '0', icon: XCircle, color: 'bg-red-500' },
]

export default function Dashboard() {
  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-8">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => (
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

      <div className="mt-8 bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          Bienvenido a ERP Paraguay
        </h2>
        <p className="text-gray-600">
          Sistema de facturación electrónica integrado con SIFEN.
        </p>
        <ul className="mt-4 space-y-2 text-sm text-gray-500">
          <li>✅ Backend Django configurado</li>
          <li>✅ Modelos de datos listos</li>
          <li>✅ Generador CDC implementado</li>
          <li>⏳ Integración SIFEN en desarrollo</li>
        </ul>
      </div>
    </div>
  )
}
