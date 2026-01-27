import { useState } from 'react'
import { Plus, Building2, MapPin, Phone, Mail } from 'lucide-react'
import { useCompanies } from '../hooks/useApi'
import CompanyForm from '../components/CompanyForm'

export default function Companies() {
  const [showForm, setShowForm] = useState(false)
  const { data: companies, isLoading, refetch } = useCompanies()

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Empresas</h1>
        <button 
          onClick={() => setShowForm(true)}
          className="flex items-center gap-2 bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors"
        >
          <Plus className="w-5 h-5" />
          Nueva Empresa
        </button>
      </div>

      {isLoading ? (
        <div className="text-center py-8 text-gray-500">Cargando...</div>
      ) : companies?.length > 0 ? (
        <div className="grid gap-4">
          {companies.map((company: {
            id: number
            ruc: string
            razon_social: string
            nombre_fantasia: string
            departamento: string
            ciudad: string
            direccion: string
            telefono: string
            email: string
            is_active: boolean
          }) => (
            <div 
              key={company.id}
              className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:border-primary-300 transition-colors"
            >
              <div className="flex justify-between items-start">
                <div>
                  <div className="flex items-center gap-3">
                    <div className="bg-primary-100 p-2 rounded-lg">
                      <Building2 className="w-5 h-5 text-primary-600" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900">{company.razon_social}</h3>
                      <p className="text-sm text-gray-500">RUC: {company.ruc}</p>
                    </div>
                  </div>
                  
                  <div className="mt-4 grid grid-cols-2 gap-4 text-sm">
                    <div className="flex items-center gap-2 text-gray-600">
                      <MapPin className="w-4 h-4" />
                      <span>{company.ciudad}, {company.departamento}</span>
                    </div>
                    {company.telefono && (
                      <div className="flex items-center gap-2 text-gray-600">
                        <Phone className="w-4 h-4" />
                        <span>{company.telefono}</span>
                      </div>
                    )}
                    <div className="flex items-center gap-2 text-gray-600">
                      <Mail className="w-4 h-4" />
                      <span>{company.email}</span>
                    </div>
                  </div>
                </div>
                
                <span className={`px-2 py-1 text-xs rounded-full ${
                  company.is_active 
                    ? 'bg-green-100 text-green-700' 
                    : 'bg-gray-100 text-gray-700'
                }`}>
                  {company.is_active ? 'Activa' : 'Inactiva'}
                </span>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200">
          <div className="p-8 text-center text-gray-500">
            <Building2 className="w-12 h-12 mx-auto mb-4 text-gray-300" />
            <p>No hay empresas registradas.</p>
            <p className="text-sm mt-2">Registra tu primera empresa para comenzar a facturar.</p>
          </div>
        </div>
      )}

      {showForm && (
        <CompanyForm 
          onClose={() => setShowForm(false)} 
          onSuccess={() => refetch()}
        />
      )}
    </div>
  )
}
