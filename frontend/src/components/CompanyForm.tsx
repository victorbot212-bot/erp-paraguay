import { useForm } from 'react-hook-form'
import { X } from 'lucide-react'
import { useDepartamentos, useCreateCompany } from '../hooks/useApi'

interface CompanyFormData {
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
}

interface Props {
  onClose: () => void
  onSuccess: () => void
}

export default function CompanyForm({ onClose, onSuccess }: Props) {
  const { register, handleSubmit, formState: { errors } } = useForm<CompanyFormData>()
  const { data: departamentos } = useDepartamentos()
  const createCompany = useCreateCompany()

  const onSubmit = async (data: CompanyFormData) => {
    try {
      await createCompany.mutateAsync(data)
      onSuccess()
      onClose()
    } catch (error) {
      console.error('Error creating company:', error)
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl shadow-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center p-6 border-b">
          <h2 className="text-xl font-semibold">Nueva Empresa</h2>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
            <X className="w-6 h-6" />
          </button>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="p-6 space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                RUC *
              </label>
              <input
                {...register('ruc', { 
                  required: 'RUC es requerido',
                  pattern: {
                    value: /^\d{1,8}-\d$/,
                    message: 'Formato: 12345678-9'
                  }
                })}
                placeholder="80012345-6"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
              {errors.ruc && (
                <p className="text-red-500 text-sm mt-1">{errors.ruc.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Timbrado
              </label>
              <input
                {...register('timbrado', { 
                  pattern: {
                    value: /^\d{8}$/,
                    message: '8 dígitos'
                  }
                })}
                placeholder="12345678"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Razón Social *
            </label>
            <input
              {...register('razon_social', { required: 'Razón social es requerida' })}
              placeholder="Mi Empresa S.A."
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
            />
            {errors.razon_social && (
              <p className="text-red-500 text-sm mt-1">{errors.razon_social.message}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Nombre Fantasía
            </label>
            <input
              {...register('nombre_fantasia')}
              placeholder="Mi Empresa"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Actividad Económica *
            </label>
            <input
              {...register('actividad_economica', { required: 'Actividad es requerida' })}
              placeholder="47111"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
            />
          </div>

          <div className="grid grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Departamento *
              </label>
              <select
                {...register('departamento', { required: true })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              >
                <option value="">Seleccionar...</option>
                {departamentos?.map((d: { codigo: string; nombre: string }) => (
                  <option key={d.codigo} value={d.nombre}>{d.nombre}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Distrito *
              </label>
              <input
                {...register('distrito', { required: true })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Ciudad *
              </label>
              <input
                {...register('ciudad', { required: true })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Dirección *
            </label>
            <textarea
              {...register('direccion', { required: true })}
              rows={2}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Teléfono
              </label>
              <input
                {...register('telefono')}
                placeholder="+595 21 123456"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Email *
              </label>
              <input
                {...register('email', { 
                  required: 'Email es requerido',
                  pattern: {
                    value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
                    message: 'Email inválido'
                  }
                })}
                type="email"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              />
              {errors.email && (
                <p className="text-red-500 text-sm mt-1">{errors.email.message}</p>
              )}
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
              disabled={createCompany.isPending}
              className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50"
            >
              {createCompany.isPending ? 'Guardando...' : 'Guardar Empresa'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
