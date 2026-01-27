# ERP Paraguay - Especificación Técnica SIFEN

## Investigación Completada: 2026-01-27

---

## 1. Hallazgos Clave de la Investigación

### 1.1 Estado Actual de SIFEN (DNIT)
- **+2,000 millones** de Documentos Electrónicos procesados
- **+20,000** contribuyentes emitiendo facturas electrónicas
- **RG 41/2025**: Proveedores del Estado obligados desde 02/01/2026
- Sistema gratuito **e-Kuatia'i** para pequeños contribuyentes

### 1.2 Recursos Técnicos Encontrados

**Repositorios GitHub relevantes:**
| Repo | Descripción | Lenguaje |
|------|-------------|----------|
| `parrawilson/sifen-py` | Módulo Python completo para SIFEN | Python |
| `fedexcde/factura-electronica-backend` | Backend API para facturación | - |
| `paulocesargarcia/sifen-kude` | Generador PDF KuDE desde XML | - |
| `ifazaSalcedo/sifenpy` | Cliente SOAP con Spring Boot | Java |

---

## 2. Estructura XML SIFEN (Manual Técnico 150)

### 2.1 Namespace y Versión
```xml
<rDE xmlns="http://ekuatia.set.gov.py/sifen/xsd"
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
     xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
  <dVerFor>150</dVerFor>
  <!-- ... -->
</rDE>
```

### 2.2 Estructura Principal del XML

```
rDE (Raíz Documento Electrónico)
├── dVerFor (Versión: "150")
└── DE (Documento Electrónico)
    ├── dDVId (Dígito Verificador)
    ├── dFecFirma (Fecha Firma)
    ├── dSisFact (Sistema Facturador)
    ├── gOpeDE (Operación del DE)
    │   ├── iTipEmi (Tipo Emisión)
    │   ├── dDesTipEmi (Descripción)
    │   ├── dCodSeg (Código Seguridad 9 dígitos)
    │   ├── dInfoEmi (Info Emisor)
    │   └── dInfoFisc (Info Fiscal)
    ├── gTimb (Timbrado)
    │   ├── iTiDE (Tipo DE)
    │   ├── dDesTiDE (Descripción Tipo)
    │   ├── dNumTim (Número Timbrado 8 dígitos)
    │   ├── dEst (Establecimiento)
    │   ├── dPunExp (Punto Expedición)
    │   ├── dNumDoc (Número Documento)
    │   ├── dSerieNum (Serie)
    │   └── dFeIniT (Fecha Inicio Vigencia)
    ├── gDatGralOpe (Datos Generales Operación)
    │   ├── dFeEmiDE (Fecha Emisión)
    │   ├── gOpeCom (Operación Comercial)
    │   │   ├── iTipTra (Tipo Transacción)
    │   │   ├── iTImp (Tipo Impuesto)
    │   │   ├── cMoneOpe (Moneda)
    │   │   └── ...
    │   ├── gEmis (Emisor)
    │   │   ├── dRucEm (RUC)
    │   │   ├── dDVEmi (DV)
    │   │   ├── iTipCont (Tipo Contribuyente)
    │   │   ├── cTipReg (Tipo Régimen)
    │   │   ├── dNomEmi (Nombre)
    │   │   └── ...
    │   └── gDatRec (Receptor)
    ├── gDtipDE (Datos Específicos por Tipo DE)
    ├── gTotSub (Totales y Subtotales)
    └── gCamGen (Campos Generales)
```

---

## 3. Modelos de Datos Python

### 3.1 Factura (Modelo Principal)
```python
@dataclass
class Factura:
    emisor: Emisor
    receptor: Receptor
    items: List[ItemFactura]
    fecha_emision: datetime
    
    # Tipos de operación
    tipo_operacion: str  # 1=B2B, 2=B2C, 3=B2G, 4=B2F
    tipo_factura: str    # 1=Factura electrónica
    moneda: str          # PYG, USD, BRL
    
    # Timbrado
    timbrado: str        # 8 dígitos
    serie_timbrado: str  # 2 caracteres
    numero_factura: str  # Formato: 001-001-0000001
    
    # Condiciones
    condicion_venta: str  # 1=Contado, 2=Crédito
    tipo_credito: str     # 1=Plazo, 2=Cuotas
    cuotas: List[Cuota]
    
    # Seguridad
    codigo_seguridad: str  # 9 dígitos aleatorios
```

### 3.2 Emisor
```python
@dataclass
class Emisor:
    ruc: str              # 8 dígitos
    dv: str               # 1 dígito verificador
    nombre: str
    nombre_fantasia: str
    direccion: str
    num_casa: str
    departamento: str     # Código DNIT
    distrito: str         # Código DNIT
    ciudad: str           # Código DNIT
    telefono: str
    email: str
    c_tipo_contribuyente: str  # 1=Persona Física, 2=Persona Jurídica
    c_tipo_regimen: str        # Régimen tributario
```

### 3.3 ItemFactura
```python
@dataclass
class ItemFactura:
    codigo: str
    descripcion: str
    cantidad: Decimal
    precio_unitario: Decimal
    unidad_medida: str     # Código DNIT
    
    # IVA
    tasa_iva: str          # 1=10%, 2=5%, 3=Exento
    monto_iva: Decimal
    
    # Descuentos
    porcentaje_descuento: Decimal
    monto_descuento: Decimal
```

---

## 4. Catálogos y Constantes DNIT

### 4.1 Tipos de Documento Electrónico
| Código | Descripción |
|--------|-------------|
| 1 | Factura electrónica |
| 2 | Factura electrónica de exportación |
| 3 | Factura electrónica de importación |
| 4 | Autofactura electrónica |
| 5 | Nota de crédito electrónica |
| 6 | Nota de débito electrónica |
| 7 | Nota de remisión electrónica |
| 8 | Comprobante de retención electrónico |

### 4.2 Tipos de Operación
| Código | Descripción |
|--------|-------------|
| 1 | B2B (Business to Business) |
| 2 | B2C (Business to Consumer) |
| 3 | B2G (Business to Government) |
| 4 | B2F (Business to Foreign) |

### 4.3 Condición de Venta
| Código | Descripción |
|--------|-------------|
| 1 | Contado |
| 2 | Crédito |

### 4.4 Tasas de IVA Paraguay
| Código | Tasa | Descripción |
|--------|------|-------------|
| 1 | 10% | Tasa general |
| 2 | 5% | Tasa reducida |
| 3 | 0% | Exento |

### 4.5 Monedas
| Código | Descripción |
|--------|-------------|
| PYG | Guaraníes |
| USD | Dólares estadounidenses |
| BRL | Reales brasileños |
| EUR | Euros |
| ARS | Pesos argentinos |

---

## 5. Generación del CDC (Código de Control)

### 5.1 Estructura (44 caracteres)
```
Posición | Longitud | Campo
---------|----------|------
1        | 2        | Tipo DE
3        | 8        | RUC Emisor
11       | 1        | DV Emisor
12       | 3        | Establecimiento
15       | 3        | Punto Expedición
18       | 7        | Número Documento
25       | 2        | Tipo Contribuyente
27       | 3        | Tipo DE (repetido)
30       | 8        | Fecha (AAAAMMDD)
38       | 9        | Número Aleatorio
```

### 5.2 Ejemplo de Generación
```python
def generar_cdc(factura):
    return (
        f"{factura.tipo_factura:02d}"           # 01
        f"{factura.emisor.ruc:08d}"             # 12345678
        f"{factura.emisor.dv}"                  # 9
        f"{establecimiento:03d}"               # 001
        f"{punto_expedicion:03d}"              # 001
        f"{numero:07d}"                        # 0000001
        f"{factura.fecha.strftime('%Y%m%d')}"  # 20260127
        f"{random_seguro(9)}"                  # 123456789
    )  # Total: 44 caracteres
```

---

## 6. Firma Digital

### 6.1 Estándar
- **XMLDSig** (Enveloped Signature)
- Certificados **PKCS#12 (.pfx/.p12)**
- Prestadores acreditados en Paraguay

### 6.2 Proceso
1. Generar XML sin firma
2. Calcular digest (SHA-256)
3. Firmar con clave privada
4. Insertar `<ds:Signature>` en XML

---

## 7. Endpoints SIFEN (Producción)

### 7.1 URLs Base
- **Producción:** `https://sifen.set.gov.py/de/ws/`
- **Test:** `https://sifen-test.set.gov.py/de/ws/`

### 7.2 Web Services
| Servicio | Descripción |
|----------|-------------|
| `siRecepDE` | Recepción de DE |
| `siRecepLote` | Recepción de Lotes |
| `siConsultaDE` | Consulta estado DE |
| `siConsultaLote` | Consulta estado Lote |
| `siConsultaRUC` | Validación RUC |
| `siEventoDE` | Eventos (cancelación, etc.) |

---

## 8. Stack Tecnológico Propuesto

### 8.1 Backend
```
Framework: Django 5.x + Django REST Framework
Base de Datos: PostgreSQL 16
Manejo XML: lxml
Firma Digital: signxml / xmlsec
Async Tasks: Celery + Redis
Cache: Redis
```

### 8.2 Frontend
```
Framework: React 18 / Next.js 14
UI Library: Ant Design 5
State: Zustand / React Query
Charts: Recharts
```

### 8.3 Infraestructura
```
Containers: Docker
Orchestration: Kubernetes / Docker Compose
Cloud: AWS / GCP
CI/CD: GitHub Actions
Monitoring: Prometheus + Grafana
```

---

## 9. Próximos Pasos

### Fase 1: MVP (Prioridad Alta)
1. [ ] Scaffolding Django + React
2. [ ] Modelos de datos (Emisor, Receptor, Factura, Items)
3. [ ] Generador XML SIFEN
4. [ ] Integración firma digital
5. [ ] API REST para facturación
6. [ ] UI básica de facturación

### Fase 2: Integración DNIT
1. [ ] Cliente SOAP para SIFEN
2. [ ] Manejo de lotes
3. [ ] Gestión de eventos
4. [ ] Generador KuDE (PDF con QR)

### Fase 3: Módulos Adicionales
1. [ ] RG 90/21 (Marangatu)
2. [ ] Reportes IVA (F120)
3. [ ] Inventario básico
4. [ ] Cuentas por cobrar/pagar

---

## 10. Referencias

- Portal e-Kuatia: https://www.dnit.gov.py/web/e-kuatia
- sifen-py (GitHub): https://github.com/parrawilson/sifen-py
- Manual Técnico 150 (buscar en DNIT)
- Namespace XSD: http://ekuatia.set.gov.py/sifen/xsd
