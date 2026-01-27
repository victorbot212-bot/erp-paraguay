"""
Catálogo de Actividades Económicas DNIT.
Códigos según clasificación CNAEP.
"""

# Subset de actividades más comunes (el catálogo completo tiene 8000+)
ACTIVIDADES_ECONOMICAS = {
    # Comercio al por menor
    "47111": "Venta al por menor en comercios no especializados con predominio de la venta de alimentos, bebidas o tabaco",
    "47112": "Venta al por menor en supermercados",
    "47113": "Venta al por menor en minimercados",
    "47190": "Venta al por menor de otros productos en comercios no especializados",
    "47211": "Venta al por menor de frutas y verduras frescas",
    "47212": "Venta al por menor de carnes",
    "47213": "Venta al por menor de productos lácteos",
    "47214": "Venta al por menor de huevos",
    "47219": "Venta al por menor de otros productos alimenticios n.c.p.",
    "47220": "Venta al por menor de bebidas en comercios especializados",
    "47300": "Venta al por menor de combustibles para vehículos automotores",
    "47411": "Venta al por menor de computadoras y equipo periférico",
    "47412": "Venta al por menor de programas informáticos",
    "47420": "Venta al por menor de equipos de telecomunicaciones",
    "47430": "Venta al por menor de equipos de sonido y video",
    "47510": "Venta al por menor de productos textiles",
    "47520": "Venta al por menor de artículos de ferretería, pinturas y productos de vidrio",
    "47530": "Venta al por menor de tapices, alfombras y cubrimientos para paredes y pisos",
    "47591": "Venta al por menor de muebles",
    "47592": "Venta al por menor de artículos de iluminación",
    "47593": "Venta al por menor de utensilios domésticos",
    "47599": "Venta al por menor de otros aparatos de uso doméstico n.c.p.",
    "47610": "Venta al por menor de libros, periódicos y artículos de papelería",
    "47620": "Venta al por menor de grabaciones de música y video",
    "47630": "Venta al por menor de equipo de deporte",
    "47640": "Venta al por menor de juegos y juguetes",
    "47711": "Venta al por menor de prendas de vestir",
    "47712": "Venta al por menor de calzado",
    "47713": "Venta al por menor de artículos de marroquinería",
    "47720": "Venta al por menor de productos farmacéuticos y medicinales",
    "47730": "Venta al por menor de productos cosméticos y de tocador",
    "47740": "Venta al por menor de artículos de óptica",
    "47750": "Venta al por menor de relojes y joyas",
    "47810": "Venta al por menor de alimentos, bebidas y tabaco en puestos de venta y mercados",
    "47820": "Venta al por menor de productos textiles, prendas de vestir y calzado en puestos de venta y mercados",
    "47890": "Venta al por menor de otros productos en puestos de venta y mercados",
    "47910": "Venta al por menor por correo o por Internet",
    "47990": "Otros tipos de venta al por menor no realizada en comercios, puestos de venta o mercados",
    
    # Comercio al por mayor
    "46100": "Venta al por mayor a cambio de una comisión o por contrato",
    "46201": "Venta al por mayor de materias primas agropecuarias",
    "46202": "Venta al por mayor de animales vivos",
    "46310": "Venta al por mayor de frutas y verduras",
    "46320": "Venta al por mayor de carne y productos cárnicos",
    "46330": "Venta al por mayor de productos lácteos, huevos y aceites",
    "46390": "Venta al por mayor no especializada de alimentos, bebidas y tabaco",
    "46410": "Venta al por mayor de productos textiles",
    "46420": "Venta al por mayor de prendas de vestir",
    "46430": "Venta al por mayor de calzado",
    "46491": "Venta al por mayor de aparatos y equipos de uso doméstico",
    "46492": "Venta al por mayor de artículos de perfumería y cosméticos",
    "46499": "Venta al por mayor de otros enseres domésticos n.c.p.",
    "46510": "Venta al por mayor de computadoras y software",
    "46520": "Venta al por mayor de equipos electrónicos y de telecomunicaciones",
    "46530": "Venta al por mayor de maquinaria y equipo agropecuario",
    "46590": "Venta al por mayor de otros tipos de maquinaria y equipo",
    "46610": "Venta al por mayor de combustibles",
    "46620": "Venta al por mayor de metales y minerales",
    "46630": "Venta al por mayor de materiales de construcción",
    "46690": "Venta al por mayor de desperdicios y desechos",
    "46900": "Venta al por mayor no especializada",
    
    # Servicios
    "62010": "Actividades de programación informática",
    "62020": "Actividades de consultoría informática",
    "62090": "Otras actividades de tecnología de la información",
    "63110": "Procesamiento de datos y hospedaje de páginas web",
    "63120": "Portales web",
    "69100": "Actividades jurídicas",
    "69200": "Actividades de contabilidad y auditoría",
    "70100": "Actividades de oficinas principales",
    "70210": "Actividades de consultoría en gestión",
    "71100": "Actividades de arquitectura e ingeniería",
    "71200": "Ensayos y análisis técnicos",
    "73110": "Publicidad",
    "73200": "Estudios de mercado y encuestas",
    "74100": "Actividades especializadas de diseño",
    "74200": "Actividades de fotografía",
    "74900": "Otras actividades profesionales, científicas y técnicas n.c.p.",
    
    # Manufactura
    "10100": "Procesamiento y conservación de carne",
    "10200": "Procesamiento y conservación de pescado",
    "10300": "Procesamiento y conservación de frutas y hortalizas",
    "10400": "Elaboración de aceites y grasas",
    "10500": "Elaboración de productos lácteos",
    "10610": "Elaboración de productos de molinería",
    "10710": "Elaboración de productos de panadería",
    "10720": "Elaboración de azúcar",
    "10730": "Elaboración de cacao, chocolate y productos de confitería",
    "10800": "Elaboración de otros productos alimenticios",
    "11010": "Destilación y mezcla de bebidas alcohólicas",
    "11020": "Elaboración de vinos",
    "11030": "Elaboración de bebidas malteadas y de malta",
    "11040": "Elaboración de bebidas no alcohólicas",
    
    # Construcción
    "41000": "Construcción de edificios",
    "42100": "Construcción de carreteras y vías de ferrocarril",
    "42200": "Construcción de proyectos de servicios públicos",
    "42900": "Construcción de otras obras de ingeniería civil",
    "43110": "Demolición",
    "43120": "Preparación del terreno",
    "43210": "Instalaciones eléctricas",
    "43220": "Instalaciones de fontanería, calefacción y aire acondicionado",
    "43290": "Otras instalaciones especializadas",
    "43300": "Terminación y acabado de edificios",
    "43900": "Otras actividades especializadas de construcción",
    
    # Transporte
    "49100": "Transporte de pasajeros por ferrocarril",
    "49211": "Transporte urbano de pasajeros",
    "49212": "Servicio de taxi",
    "49221": "Transporte interurbano de pasajeros",
    "49222": "Transporte internacional de pasajeros",
    "49230": "Transporte de carga por carretera",
    "52100": "Almacenamiento y depósito",
    "52210": "Actividades de servicios vinculadas al transporte terrestre",
    "53100": "Actividades postales",
    "53200": "Actividades de mensajería",
    
    # Alojamiento y restaurantes
    "55100": "Actividades de alojamiento para estancias cortas",
    "55900": "Otros tipos de alojamiento",
    "56101": "Restaurantes",
    "56102": "Servicios de comida preparada",
    "56210": "Suministro de comidas por encargo",
    "56290": "Otros servicios de comidas",
    "56300": "Servicio de bebidas",
    
    # Educación
    "85100": "Enseñanza preescolar y primaria",
    "85200": "Enseñanza secundaria",
    "85310": "Enseñanza superior universitaria",
    "85320": "Enseñanza superior no universitaria",
    "85410": "Educación deportiva y recreativa",
    "85420": "Educación cultural",
    "85490": "Otros tipos de enseñanza n.c.p.",
    "85500": "Actividades de apoyo a la educación",
    
    # Salud
    "86100": "Actividades de hospitales",
    "86210": "Actividades de médicos y odontólogos",
    "86900": "Otras actividades de atención de la salud humana",
}


def get_actividad(codigo: str) -> str:
    """Get activity description by code."""
    return ACTIVIDADES_ECONOMICAS.get(str(codigo), "Actividad no especificada")


def buscar_actividad(termino: str) -> list:
    """Search activities by term (partial match, min 2 chars)."""
    if len(termino) < 2:
        return []
    
    termino_lower = termino.lower()
    resultados = []
    for codigo, descripcion in ACTIVIDADES_ECONOMICAS.items():
        if termino_lower in descripcion.lower():
            resultados.append({"codigo": codigo, "descripcion": descripcion})
    return resultados[:20]  # Limit results
