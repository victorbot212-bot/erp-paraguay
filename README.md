# ERP Paraguay 🇵🇾

Sistema de facturación electrónica integrado con SIFEN (Sistema Integrado de Facturación Electrónica Nacional).

## Stack Tecnológico

- **Backend:** Django 5.0 + Django REST Framework
- **Frontend:** React 18 + TypeScript + Vite
- **Base de datos:** PostgreSQL 15
- **Cola de tareas:** Celery + Redis
- **Contenedores:** Docker + Docker Compose

## Estructura del Proyecto

```
erp-paraguay/
├── backend/           # Django API
│   ├── core/          # Configuración base
│   ├── companies/     # Gestión de empresas
│   ├── invoicing/     # Facturación electrónica
│   └── sifen/         # Integración SIFEN
├── frontend/          # React SPA
│   └── src/
├── docs/              # Documentación técnica
└── docker/            # Configuración Docker
```

## Requisitos

- Python 3.11+
- Node.js 20+
- PostgreSQL 15+
- Redis 7+

## Inicio Rápido

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Frontend
cd frontend
npm install
npm run dev
```

## Documentación

- [Requisitos del Sistema](./REQUIREMENTS.md)
- [Especificación Técnica](./TECHNICAL_SPEC.md)

## Licencia

MIT
