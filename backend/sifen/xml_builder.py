"""
XML Builder for SIFEN Documents.
Based on Manual Técnico v150.

Generates the DE (Documento Electrónico) XML structure.
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from lxml import etree

# SIFEN Namespace
SIFEN_NS = "http://ekuatia.set.gov.py/sifen/xsd"
NSMAP = {None: SIFEN_NS}


class SifenXMLBuilder:
    """Builder for SIFEN XML documents."""
    
    def __init__(self):
        self.root = None
    
    def build_de(
        self,
        # CDC and document info
        cdc: str,
        tipo_de: int,
        fecha_emision: datetime,
        
        # Emisor (Company)
        emisor_ruc: str,
        emisor_razon_social: str,
        emisor_nombre_fantasia: str,
        emisor_actividad: str,
        emisor_timbrado: str,
        emisor_establecimiento: str,
        emisor_punto: str,
        emisor_numero: int,
        emisor_direccion: str,
        emisor_departamento: str,
        emisor_distrito: str,
        emisor_ciudad: str,
        emisor_telefono: str = "",
        emisor_email: str = "",
        
        # Receptor (Customer)
        receptor_contribuyente: bool = True,
        receptor_ruc: str = "",
        receptor_razon_social: str = "",
        receptor_direccion: str = "",
        receptor_email: str = "",
        receptor_tipo_doc: int = 1,  # 1=CI, 2=Pasaporte, etc.
        receptor_num_doc: str = "",
        
        # Totals
        moneda: str = "PYG",
        tipo_cambio: Decimal = Decimal("1"),
        total_bruto: Decimal = Decimal("0"),
        total_descuento: Decimal = Decimal("0"),
        total_neto: Decimal = Decimal("0"),
        total_iva_10: Decimal = Decimal("0"),
        total_iva_5: Decimal = Decimal("0"),
        total_exento: Decimal = Decimal("0"),
        total_iva: Decimal = Decimal("0"),
        total: Decimal = Decimal("0"),
        
        # Items
        items: Optional[list] = None,
        
        # Optional
        tipo_emision: int = 1,  # 1=Normal, 2=Contingencia
    ) -> etree._Element:
        """
        Build the complete DE XML structure.
        
        Returns:
            lxml Element ready for signing.
        """
        items = items or []
        
        # Root element: rDE (Raíz Documento Electrónico)
        self.root = etree.Element("rDE", nsmap=NSMAP)
        
        # dVerFor - Versión del formato
        etree.SubElement(self.root, "dVerFor").text = "150"
        
        # DE - Documento Electrónico
        de = etree.SubElement(self.root, "DE")
        de.set("Id", cdc)  # CDC as XML ID for signing
        
        # gOpeDE - Datos de la operación
        g_ope_de = etree.SubElement(de, "gOpeDE")
        etree.SubElement(g_ope_de, "iTipEmi").text = str(tipo_emision)
        etree.SubElement(g_ope_de, "dDesTipEmi").text = "Normal" if tipo_emision == 1 else "Contingencia"
        etree.SubElement(g_ope_de, "dCodSeg").text = cdc[34:43]  # Security code from CDC
        etree.SubElement(g_ope_de, "dInfoEmi").text = "1"  # Info del emisor
        
        # gTimb - Datos del timbrado
        g_timb = etree.SubElement(de, "gTimb")
        etree.SubElement(g_timb, "iTiDE").text = str(tipo_de)
        etree.SubElement(g_timb, "dDesTiDE").text = self._get_tipo_de_desc(tipo_de)
        etree.SubElement(g_timb, "dNumTim").text = emisor_timbrado
        etree.SubElement(g_timb, "dEst").text = emisor_establecimiento
        etree.SubElement(g_timb, "dPunExp").text = emisor_punto
        etree.SubElement(g_timb, "dNumDoc").text = str(emisor_numero).zfill(7)
        etree.SubElement(g_timb, "dFeIniT").text = "2024-01-01"  # TODO: from company
        
        # gDatGralOpe - Datos generales de la operación
        g_dat_gral = etree.SubElement(de, "gDatGralOpe")
        etree.SubElement(g_dat_gral, "dFeEmiDE").text = fecha_emision.strftime("%Y-%m-%dT%H:%M:%S")
        
        # gOpeCom - Operación comercial
        g_ope_com = etree.SubElement(g_dat_gral, "gOpeCom")
        etree.SubElement(g_ope_com, "iTipTra").text = "1"  # 1=Venta
        etree.SubElement(g_ope_com, "dDesTipTra").text = "Venta de mercadería"
        etree.SubElement(g_ope_com, "iTImp").text = "1"  # 1=IVA
        etree.SubElement(g_ope_com, "dDesTImp").text = "IVA"
        etree.SubElement(g_ope_com, "cMoneOpe").text = moneda
        etree.SubElement(g_ope_com, "dDesMoneOpe").text = "Guarani" if moneda == "PYG" else moneda
        
        # gEmis - Datos del emisor
        g_emis = etree.SubElement(g_dat_gral, "gEmis")
        ruc_parts = emisor_ruc.split("-")
        etree.SubElement(g_emis, "dRucEm").text = ruc_parts[0]
        etree.SubElement(g_emis, "dDVEmi").text = ruc_parts[1]
        etree.SubElement(g_emis, "iTipCont").text = "2"  # 2=Persona Jurídica
        etree.SubElement(g_emis, "dNomEmi").text = emisor_razon_social
        if emisor_nombre_fantasia:
            etree.SubElement(g_emis, "dNomFanEmi").text = emisor_nombre_fantasia
        etree.SubElement(g_emis, "dDirEmi").text = emisor_direccion
        etree.SubElement(g_emis, "dNumCas").text = "0"
        etree.SubElement(g_emis, "cDepEmi").text = self._get_depto_code(emisor_departamento)
        etree.SubElement(g_emis, "dDesDepEmi").text = emisor_departamento
        etree.SubElement(g_emis, "cDisEmi").text = "1"  # TODO: from catalog
        etree.SubElement(g_emis, "dDesDisEmi").text = emisor_distrito
        etree.SubElement(g_emis, "cCiuEmi").text = "1"  # TODO: from catalog
        etree.SubElement(g_emis, "dDesCiuEmi").text = emisor_ciudad
        if emisor_telefono:
            etree.SubElement(g_emis, "dTelEmi").text = emisor_telefono
        if emisor_email:
            etree.SubElement(g_emis, "dEmailE").text = emisor_email
        
        # gActEco - Actividad económica
        g_act_eco = etree.SubElement(g_emis, "gActEco")
        etree.SubElement(g_act_eco, "cActEco").text = emisor_actividad
        etree.SubElement(g_act_eco, "dDesActEco").text = "Actividad principal"
        
        # gDatRec - Datos del receptor
        g_dat_rec = etree.SubElement(g_dat_gral, "gDatRec")
        etree.SubElement(g_dat_rec, "iNatRec").text = "1" if receptor_contribuyente else "2"
        
        if receptor_contribuyente and receptor_ruc:
            rec_ruc_parts = receptor_ruc.split("-")
            etree.SubElement(g_dat_rec, "iTiOpe").text = "1"  # B2B
            etree.SubElement(g_dat_rec, "dRucRec").text = rec_ruc_parts[0]
            etree.SubElement(g_dat_rec, "dDVRec").text = rec_ruc_parts[1]
        else:
            etree.SubElement(g_dat_rec, "iTiOpe").text = "2"  # B2C
            if receptor_num_doc:
                etree.SubElement(g_dat_rec, "iTipIDRec").text = str(receptor_tipo_doc)
                etree.SubElement(g_dat_rec, "dNumIDRec").text = receptor_num_doc
        
        etree.SubElement(g_dat_rec, "dNomRec").text = receptor_razon_social or "Sin Nombre"
        if receptor_direccion:
            etree.SubElement(g_dat_rec, "dDirRec").text = receptor_direccion
        if receptor_email:
            etree.SubElement(g_dat_rec, "dEmailRec").text = receptor_email
        
        # gDtipDE - Datos específicos por tipo de DE
        g_dtip_de = etree.SubElement(de, "gDtipDE")
        
        # gCamFE - Campos de Factura Electrónica
        if tipo_de in [1, 2, 3]:  # Facturas
            g_cam_fe = etree.SubElement(g_dtip_de, "gCamFE")
            etree.SubElement(g_cam_fe, "iIndPres").text = "1"  # Presencial
            etree.SubElement(g_cam_fe, "dDesIndPres").text = "Operación presencial"
        
        # gCamItem - Items
        for idx, item in enumerate(items, 1):
            self._add_item(de, idx, item)
        
        # gTotSub - Subtotales
        g_tot_sub = etree.SubElement(de, "gTotSub")
        etree.SubElement(g_tot_sub, "dSubExe").text = str(total_exento)
        etree.SubElement(g_tot_sub, "dSub5").text = str(total_iva_5)
        etree.SubElement(g_tot_sub, "dSub10").text = str(total_iva_10)
        etree.SubElement(g_tot_sub, "dTotOpe").text = str(total)
        etree.SubElement(g_tot_sub, "dTotDesc").text = str(total_descuento)
        etree.SubElement(g_tot_sub, "dTotDescGloworItem").text = str(total_descuento)
        etree.SubElement(g_tot_sub, "dTotAntworItem").text = "0"
        etree.SubElement(g_tot_sub, "dTotAnt").text = "0"
        etree.SubElement(g_tot_sub, "dPorcDescTotal").text = "0"
        etree.SubElement(g_tot_sub, "dDescTotal").text = str(total_descuento)
        etree.SubElement(g_tot_sub, "dAnticipo").text = "0"
        etree.SubElement(g_tot_sub, "dRewordon").text = "0"
        etree.SubElement(g_tot_sub, "dComi").text = "0"
        etree.SubElement(g_tot_sub, "dTotGralOpe").text = str(total)
        
        # IVA totals
        if total_iva_10 > 0 or total_iva_5 > 0:
            etree.SubElement(g_tot_sub, "dIVA5").text = str(self._calc_iva(total_iva_5, 5))
            etree.SubElement(g_tot_sub, "dIVA10").text = str(self._calc_iva(total_iva_10, 10))
            etree.SubElement(g_tot_sub, "dTotIVA").text = str(
                self._calc_iva(total_iva_5, 5) + self._calc_iva(total_iva_10, 10)
            )
        
        return self.root
    
    def _add_item(self, parent: etree._Element, index: int, item: dict):
        """Add an item to the XML."""
        g_cam_item = etree.SubElement(parent, "gCamItem")
        etree.SubElement(g_cam_item, "dCodInt").text = item.get("codigo", str(index))
        
        # gValorItem
        g_valor = etree.SubElement(g_cam_item, "gValorItem")
        
        # gValorReworSItem - Valores unitarios
        g_valor_unit = etree.SubElement(g_valor, "gValorReworSItem")
        etree.SubElement(g_valor_unit, "dPUniProworSer").text = str(item["precio_unitario"])
        
        # gValPreworSIt
        g_val_pre = etree.SubElement(g_valor_unit, "gValPreworSIt")
        etree.SubElement(g_val_pre, "dDescItem").text = item["descripcion"]
        etree.SubElement(g_val_pre, "dCantProworSer").text = str(item["cantidad"])
        etree.SubElement(g_val_pre, "cUniMed").text = "77"  # UNI
        etree.SubElement(g_val_pre, "dDesUniMed").text = item.get("unidad_medida", "Unidad")
        etree.SubElement(g_val_pre, "dTotBruOpeItem").text = str(item["subtotal"])
        
        # gCamIVA - IVA del item
        g_cam_iva = etree.SubElement(g_cam_item, "gCamIVA")
        tasa = item.get("tasa_iva", 10)
        etree.SubElement(g_cam_iva, "iAfecIVA").text = "1" if tasa > 0 else "3"
        etree.SubElement(g_cam_iva, "dDesAfecIVA").text = (
            "Gravado IVA" if tasa > 0 else "Exento"
        )
        etree.SubElement(g_cam_iva, "dPropIVA").text = "100"
        etree.SubElement(g_cam_iva, "dTasaIVA").text = str(tasa)
        etree.SubElement(g_cam_iva, "dBasGravIVA").text = str(
            item["subtotal"] - item.get("iva", 0)
        )
        etree.SubElement(g_cam_iva, "dLiqIVAItem").text = str(item.get("iva", 0))
    
    def _get_tipo_de_desc(self, tipo: int) -> str:
        """Get document type description."""
        tipos = {
            1: "Factura electrónica",
            2: "Factura electrónica de exportación",
            3: "Factura electrónica de importación",
            4: "Autofactura electrónica",
            5: "Nota de crédito electrónica",
            6: "Nota de débito electrónica",
            7: "Nota de remisión electrónica",
        }
        return tipos.get(tipo, "Factura electrónica")
    
    def _get_depto_code(self, depto: str) -> str:
        """Get department code."""
        # Simplified - should use full catalog
        deptos = {
            "CAPITAL": "0",
            "ASUNCION": "0", 
            "CONCEPCION": "1",
            "SAN PEDRO": "2",
            "CORDILLERA": "3",
            "GUAIRA": "4",
            "CAAGUAZU": "5",
            "CAAZAPA": "6",
            "ITAPUA": "7",
            "MISIONES": "8",
            "PARAGUARI": "9",
            "ALTO PARANA": "10",
            "CENTRAL": "11",
            "ÑEEMBUCU": "12",
            "AMAMBAY": "13",
            "CANINDEYU": "14",
            "PTE. HAYES": "15",
            "BOQUERON": "16",
            "ALTO PARAGUAY": "17",
        }
        return deptos.get(depto.upper(), "11")  # Default Central
    
    def _calc_iva(self, base: Decimal, tasa: int) -> Decimal:
        """Calculate IVA from base (IVA included)."""
        if tasa == 0:
            return Decimal("0")
        return base - (base / (1 + Decimal(tasa) / 100))
    
    def to_string(self, pretty: bool = False) -> str:
        """Convert XML to string."""
        return etree.tostring(
            self.root,
            encoding="UTF-8",
            xml_declaration=True,
            pretty_print=pretty
        ).decode("UTF-8")
