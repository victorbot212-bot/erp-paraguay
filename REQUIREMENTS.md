# ERP Paraguay - Biblia del Proyecto

## 1. Visión Ejecutiva y Contexto Estratégico

El mercado de software de gestión empresarial en Paraguay atraviesa un punto de inflexión histórico. La convergencia de mandatos gubernamentales agresivos hacia la digitalización fiscal, liderados por la Dirección Nacional de Ingresos Tributarios (DNIT), y una generación emergente de empresarios que exigen movilidad y experiencia de usuario (UX) de clase mundial, ha creado una ventana de oportunidad crítica.

### Objetivo
Desarrollar un sistema de Planificación de Recursos Empresariales (ERP) web que desplace a los actores establecidos como Starsoft, Inventiva e Ignis.

### Visión
"Sistema Operativo de Negocios" nativo en la nube:
- Arquitectura API-first
- Resolver la fricción del cumplimiento tributario (SIFEN, RG 90/21, IRE, IPS)
- Integración invisible en la operación diaria
- Plataforma SaaS escalable

### Target
- Pequeñas empresas de servicios
- Medianas industrias importadoras

## 2. Análisis Competitivo

### 2.1.1. Starsoft Paraguay (El Gigante)

**Fortalezas:**
- Estándar de facto en sector contable
- Profundidad funcional en contabilidad
- Manejo de casuísticas complejas IRE/IVA
- 20 años de funcionalidad probada
- "Gold Edition" y "Expert 360" (intentos de nube)

**Debilidades Críticas:**
- Soporte técnico lento y deficiente
- Arquitectura web = adaptación de escritorio
- Falta fluidez de app nativa moderna
- Problemas compatibilidad de versiones
- Dependencia actualizaciones manuales

**Estrategia de Desplazamiento:**
- "Soporte como Funcionalidad" con chat integrado
- Documentación de autocuración
- SLA garantizados
- Interfaz radicalmente intuitiva
- Eliminar necesidad de capacitación intensiva

---

## Requisitos Técnicos Clave (Paraguay)

### Cumplimiento Fiscal Obligatorio
- **SIFEN** - Sistema Integrado de Facturación Electrónica Nacional
- **RG 90/21** - Resolución General sobre facturación
- **IRE** - Impuesto a la Renta Empresarial
- **IPS** - Instituto de Previsión Social
- **DNIT** - Dirección Nacional de Ingresos Tributarios

### 2.1.2. Inventiva (Solución Corporativa)

**Fortalezas:**
- Posicionado en segmento medio-alto/corporativo
- Tecnología Oracle como estandarte
- 100+ módulos (cooperativas, centros comerciales, maquiladoras)
- Percepción de seguridad y escalabilidad

**Debilidades Críticas:**
- Complejidad excesiva
- Costos elevados de licencias Oracle
- Tiempos de implementación largos
- Curva de aprendizaje empinada
- Sobredimensionado para PYMEs

**Estrategia de Desplazamiento:**
- PostgreSQL (código abierto, grado empresarial) → reducir TCO
- Arquitectura modular real ("encender" solo lo necesario)
- Evitar bloatware

### 2.1.3. Retadores y Nichos

**Ignis:** Soluciones de nicho, hay espacio para software especializado

**Enconapp y Apps Ligeras:**
- Nueva ola de apps móviles para microempresas
- Excelente UX
- Deficientes en profundidad contable y cumplimiento tributario

**Interfaces (Odoo):**
- ERP global código abierto
- Fortaleza: tecnología mundial
- Debilidad: localización Paraguay (SIFEN, Tesaka, RG90)
- Se rompe con actualizaciones del núcleo

**Estrategia de Desplazamiento:**
- Combinar UX de Enconapp + profundidad de Starsoft
- Conformidad DNIT nativa desde "Día Cero"
- No parches de terceros

## 2.2. Brecha de Oportunidad (Blue Ocean)

**NO existe un ERP Web Nativo Paraguayo que combine:**
- UX tipo Silicon Valley
- Rigurosidad fiscal absoluta

Los sistemas actuales son:
- "Dinosaurios potentes" (Starsoft, Inventiva)
- "Juguetes bonitos" (apps ligeras)

### Matriz Comparativa

| Característica | Starsoft/Inventiva | Apps Ligeras/Excel | **NUEVO ERP** |
|---|---|---|---|
| Arquitectura | Híbrida/Desktop | Nube Simple | **SaaS Nativo/Micro-Modular** |
| UX/UI | Compleja, Windows | Moderna, Limitada | **Diseño 2026, Modo Oscuro, AI** |
| Implementación | Meses, Consultores | Inmediata | **Self-Onboarding + Migración Auto** |
| Cumplimiento | Robusto pero Manual | Básico/Inexistente | **Automatización SIFEN/RG90** |
| Costo Inicial | Alto (Licencias+HW) | Bajo/Gratis | **Suscripción Mensual Escalable** |

---

## 3. Núcleo Regulatorio: DNIT y SIFEN

> En Paraguay, un ERP no es útil si no es un motor de cumplimiento tributario.

La integración con SIFEN y cumplimiento DNIT deben ser **el corazón del sistema**, no un módulo periférico.

### 3.1. Arquitectura de Facturación Electrónica (SIFEN)

El sistema debe ser **emisor autorizado e-Kuatia** (software propio), no e-Kuatia'i (gratuito).

#### 3.1.1. Ciclo de Vida del Documento Electrónico (DE)

**1. Generación del XML:**
- Seguir esquemas XSD del **Manual Técnico 150**
- Validar tipos de datos, longitudes, catálogos
- Actividades económicas, unidades de medida

**2. Generación del CDC (Código de Control) - 44 dígitos:**
```
Tipo(2) + RUC(8) + DV(1) + Est(3) + PtoExp(3) + Num(7) + 
TipoDoc(3) + Serie(2) + Fecha(8) + Aleatorio(9) + DV(1)
```
⚠️ **CRÍTICO:** Generador aleatorio criptográficamente seguro para evitar colisiones

**3. Firma Digital:**
- Estándar **XMLDSig (Enveloped)**
- Certificados **PKCS#12 (.pfx)** de prestadores acreditados Paraguay
- Gestión segura de claves privadas en nube → **KMS (Key Management Service)**

**4. Generación del KuDE (QR):**
- Cadena dinámica: URL DNIT + CDC + Fecha + RUC receptor + Totales + Digest Value

#### 3.1.2. Transmisión Asíncrona y Manejo de Eventos

**Modelo asíncrono para lotes:**
1. Enviar lote → recibir `dId` (ID de lote)
2. Polling recursivo hasta: `Approved` | `Rejected` | `Approved with Observations`

**Gestión de Fallos:**
- Traducir códigos error técnicos → lenguaje humano
- Permitir corrección y reenvío sin perder datos

**Eventos Tributarios:**
- ✅ Cancelación
- ✅ Inutilización de numeración
- ✅ Nota de Remisión Electrónica
- ✅ Conformidad del receptor

---

## 3.2. Obligaciones Tributarias: IVA, IRE y RG 90/21

### RG 90/21 (Registro Electrónico) ⚠️ PUNTO CRÍTICO DE DOLOR
- Generar automáticamente archivos JSON/Excel para **Marangatu**
- Clasificar cada gasto/ingreso según códigos DNIT
- Registro mensual de comprobantes

### Formularios 500 y 501 (IRE)
- Régimen General y Simple
- **Calcular automáticamente deducibilidad** de gastos
- Limitar gastos personales o sin documentación válida
- Generar borradores de balances impositivos
- Cuadros de depreciación de activos fijos

### IVA (Formulario 120)
- **Cálculo automático de prorrateo** IVA crédito fiscal
- Para empresas con ingresos mixtos (gravados + exentos)
- Operación compleja, propensa a errores manuales

---

## 3.3. Normativa Laboral y Previsional (IPS/MTESS)

### Cálculos de IPS
| Concepto | Porcentaje |
|---|---|
| Aporte Obrero | 9% |
| Aporte Patronal | 16.5% |

- Parametrizados pero **configurables**
- Generar archivo automático para sistema **REI del IPS**

### Aguinaldo (13er Salario)
- Sumar remuneraciones devengadas: salario + horas extras + comisiones
- Dividir por 12
- **Auditar** que no se incluyan conceptos no remunerativos erróneos
- Proteger empresa de multas laborales

### Digitalización Laboral
- Archivos para planillas anuales MTESS

---

## 4. Arquitectura Funcional: Estructura Modular

### 4.1. Módulo Financiero y Contable (El Cerebro)

**Multimoneda Real:**
- Guaraníes, Dólares, Reales
- Sincronizar cotización diaria con API BCP
- Calcular diferencias de cambio automáticamente

**Plan de Cuentas Inteligente:**
- Pre-cargado con plantillas paraguayas
- Totalmente flexible

**Conciliación Bancaria Automática:**
- Importar extractos (OFX/Excel)
- Conciliación asistida por IA

**Gestión de Cheques Diferidos:**
- Dashboard específico
- Alertas de vencimiento
- Crucial para flujo de caja

### 4.2. Módulo Comercial y Facturación (El Motor)

**POS Web:**
- Interfaz táctil + teclado
- **OFFLINE-FIRST** ⚠️ (crítico para Paraguay)
- Sincroniza XMLs al recuperar conexión

**CRM Integrado:**
- Historial de compras
- Límites de crédito (bloqueo automático)
- **Integración WhatsApp API** → enviar presupuestos/facturas

**Tesaka Legacy:**
- Importar datos históricos
- Gestión híbrida para transición

### 4.3. Módulo de Inventario y Logística (El Esqueleto)

**Costeo de Importaciones (KILLER FEATURE):**
- Prorratear: despacho aduanero + fletes + seguros sobre FOB
- Actualizar PPP real en guaraníes

**Multidepósito y Trazabilidad:**
- Múltiples sucursales
- Depósitos virtuales ("Mercadería en Tránsito")
- Lotes y fechas vencimiento (FEFO)

**WMS Ligero:**
- Colectores Android
- Picking y toma de inventario

### 4.4. Módulo de Recursos Humanos

- Liquidación de salarios (PDF legal)
- Control de asistencia (biométrico/web/móvil con geolocalización)
- Gestión de préstamos y anticipos (descuento automático)

---

## 5. Especificaciones Técnicas y Stack

### 5.1. Paradigma: MONOLITO MODULAR

**Justificación:**
- Reduce complejidad DevOps
- Reduce latencia de red
- Módulos como dominios lógicos separados
- Integridad referencial de datos transaccionales
- Extraer microservicios después si necesario (ej: validador SIFEN)

### 5.2. Stack Tecnológico

| Capa | Tecnología | Justificación |
|---|---|---|
| **Backend** | Python (Django/FastAPI) | Manejo XML, Admin out-of-box, seguridad |
| **Frontend** | React.js o Vue.js | SPA, velocidad de entrada de datos |
| **UI Library** | Ant Design / Material UI | Acelerar desarrollo |
| **Base de Datos** | PostgreSQL | JSONB para respuestas XML variables |
| **Infraestructura** | Docker + Kubernetes | AWS o GCP |

### 5.3. Seguridad

- **Encriptación reposo:** AES-256
- **Encriptación tránsito:** TLS 1.3
- **Autenticación:** OAuth2 + 2FA obligatorio para admins
- **Audit Trails:** Registro inmutable (quién, qué, cuándo)
- Instantánea antes/después de cambios contables

---

## 6. Estrategia UX/UI 2025/2026

### 6.1. Filosofía: "Carga Cognitiva Mínima"

**Command Palette (Ctrl+K):**
- Navegar sin menús jerárquicos
- "Nueva Factura", "Reporte IVA", "Buscar Cliente X"

**Dashboards Operativos:**
- KPIs al iniciar: Ventas del día, Cuentas vencidas, Saldo bancos
- Widgets interactivos y personalizables

**Modo Oscuro:** Esencial para uso prolongado

### 6.2. Visualización Financiera

**Jerarquía Visual por Colores:**
- 🔴 Rojo: Vencido/Rechazado SIFEN
- 🟢 Verde: Cobrado/Aprobado
- 🟠 Naranja: Pendiente

**Tablas Inteligentes:**
- Ordenar, filtrar, ocultar columnas
- Exportar Excel directo

### 6.3. Experiencia Móvil

**Vistas específicas (no encoger desktop):**
- Aprobaciones gerenciales
- Ventas en ruta (pedidos/cobros)

---

## 7. Modelo de Negocio SaaS

### 7.1. Niveles de Precio

| Nivel | Target | Precio | Incluye |
|---|---|---|---|
| **Micro** | Unipersonales | Freemium/Bajo | Facturación básica, IVA |
| **PYME** | Pequeñas empresas | 250-500k Gs/mes | Inventario, ctas ctes, multi-usuario |
| **Corporativo** | Medianas+ | Personalizado | API, sucursales, centros de costo |

### 7.2. Onboarding y Migración

**"Importación Mágica":**
- Leer Excel exportados de Starsoft
- Leer archivos Hechauka/Marangatu
- Poblar clientes, productos, saldos en minutos

---

## 8. Roadmap de Implementación

### Fase 1: MVP (Mes 1-4)
- [ ] Autenticación y seguridad
- [ ] Facturación Electrónica SIFEN (emisión básica)
- [ ] Gestión Clientes y Productos
- [ ] Reportes IVA (F120)

### Fase 2: Consolidación (Mes 5-8)
- [ ] Módulo Compras y Cuentas a Pagar
- [ ] Inventario básico
- [ ] Integración RG 90/21 (Marangatu)
- [ ] Beta con "Friendly Users"

### Fase 3: Expansión (Mes 9-12)
- [ ] Módulo Contable completo
- [ ] Recursos Humanos e IPS
- [ ] App Móvil
- [ ] API Pública

---

## 9. Conclusión

> La clave no está solo en el código, sino en entender que para el empresario paraguayo, **el mejor software es aquel que transforma la obligación tributaria en una ventaja administrativa invisible.**

Este ERP debe ser el nuevo estándar del mercado paraguayo.
