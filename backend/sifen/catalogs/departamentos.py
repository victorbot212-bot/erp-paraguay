"""
Catálogo de Departamentos y Distritos de Paraguay.
Basado en catálogo DNIT para SIFEN.
"""

DEPARTAMENTOS = {
    "0": {
        "nombre": "CAPITAL",
        "distritos": {
            "1": "ASUNCION",
        }
    },
    "1": {
        "nombre": "CONCEPCION",
        "distritos": {
            "1": "CONCEPCION",
            "2": "BELEN",
            "3": "HORQUETA",
            "4": "LORETO",
            "5": "SAN CARLOS DEL APA",
            "6": "SAN LAZARO",
            "7": "YBY YAU",
            "8": "AZOTEY",
            "9": "PASO BARRETO",
            "10": "SARGENTO JOSE FELIX LOPEZ",
        }
    },
    "2": {
        "nombre": "SAN PEDRO",
        "distritos": {
            "1": "SAN PEDRO DEL YCUAMANDIYU",
            "2": "ANTEQUERA",
            "3": "CHORE",
            "4": "GENERAL ELIZARDO AQUINO",
            "5": "ITACURUBI DEL ROSARIO",
            "6": "LIMA",
            "7": "NUEVA GERMANIA",
            "8": "SAN ESTANISLAO",
            "9": "SAN PABLO",
            "10": "TACUATI",
            "11": "UNION",
            "12": "25 DE DICIEMBRE",
            "13": "VILLA DEL ROSARIO",
            "14": "GENERAL ISIDORO RESQUIN",
            "15": "YATAITY DEL NORTE",
            "16": "GUAYAIBI",
            "17": "CAPIIBARY",
            "18": "SANTA ROSA DEL AGUARAY",
            "19": "YRYBUCUA",
            "20": "LIBERACION",
        }
    },
    "3": {
        "nombre": "CORDILLERA",
        "distritos": {
            "1": "CAACUPE",
            "2": "ALTOS",
            "3": "ARROYOS Y ESTEROS",
            "4": "ATYRA",
            "5": "CARAGUATAY",
            "6": "EMBOSCADA",
            "7": "EUSEBIO AYALA",
            "8": "ISLA PUCU",
            "9": "ITACURUBI DE LA CORDILLERA",
            "10": "JUAN DE MENA",
            "11": "LOMA GRANDE",
            "12": "MBOCAYATY DEL YHAGUY",
            "13": "NUEVA COLOMBIA",
            "14": "PIRIBEBUY",
            "15": "PRIMERO DE MARZO",
            "16": "SAN BERNARDINO",
            "17": "SAN JOSE OBRERO",
            "18": "SANTA ELENA",
            "19": "TOBATI",
            "20": "VALENZUELA",
        }
    },
    "4": {
        "nombre": "GUAIRA",
        "distritos": {
            "1": "VILLARRICA",
            "2": "BORJA",
            "3": "CAPITAN MAURICIO JOSE TROCHE",
            "4": "CORONEL MARTINEZ",
            "5": "FELIX PEREZ CARDOZO",
            "6": "GENERAL EUGENIO A. GARAY",
            "7": "INDEPENDENCIA",
            "8": "ITAPE",
            "9": "ITURBE",
            "10": "JOSE FASSARDI",
            "11": "MBOCAYATY",
            "12": "NATALICIO TALAVERA",
            "13": "ÑUMI",
            "14": "SAN SALVADOR",
            "15": "YATAITY",
            "16": "DOCTOR BOTTRELL",
            "17": "PASO YOBAI",
            "18": "TEBICUARY",
        }
    },
    "5": {
        "nombre": "CAAGUAZU",
        "distritos": {
            "1": "CORONEL OVIEDO",
            "2": "CAAGUAZU",
            "3": "CARAYAO",
            "4": "DOCTOR CECILIO BAEZ",
            "5": "SANTA ROSA DEL MBUTUY",
            "6": "DR. JUAN MANUEL FRUTOS",
            "7": "REPATRIACION",
            "8": "NUEVA LONDRES",
            "9": "SAN JOAQUIN",
            "10": "SAN JOSE DE LOS ARROYOS",
            "11": "YHU",
            "12": "J. EULOGIO ESTIGARRIBIA",
            "13": "R.I. 3 CORRALES",
            "14": "RAUL ARSENIO OVIEDO",
            "15": "JOSE DOMINGO OCAMPOS",
            "16": "MARISCAL FRANCISCO SOLANO LOPEZ",
            "17": "LA PASTORA",
            "18": "3 DE FEBRERO",
            "19": "SIMON BOLIVAR",
            "20": "VAQUERIA",
            "21": "TEMBIAPORA",
            "22": "NUEVA TOLEDO",
        }
    },
    "6": {
        "nombre": "CAAZAPA",
        "distritos": {
            "1": "CAAZAPA",
            "2": "ABAI",
            "3": "BUENA VISTA",
            "4": "DR. MOISES S. BERTONI",
            "5": "GENERAL HIGINIO MORINIGO",
            "6": "MACIEL",
            "7": "SAN JUAN NEPOMUCENO",
            "8": "TAVAI",
            "9": "YUTY",
            "10": "3 DE MAYO",
            "11": "FULGENCIO YEGROS",
        }
    },
    "7": {
        "nombre": "ITAPUA",
        "distritos": {
            "1": "ENCARNACION",
            "2": "BELLA VISTA",
            "3": "CAMBYRETA",
            "4": "CAPITAN MEZA",
            "5": "CAPITAN MIRANDA",
            "6": "NUEVA ALBORADA",
            "7": "CARMEN DEL PARANA",
            "8": "CORONEL BOGADO",
            "9": "CARLOS ANTONIO LOPEZ",
            "10": "NATALIO",
            "11": "FRAM",
            "12": "GENERAL ARTIGAS",
            "13": "GENERAL DELGADO",
            "14": "HOHENAU",
            "15": "JESUS",
            "16": "LEANDRO OVIEDO",
            "17": "OBLIGADO",
            "18": "MAYOR OTAÑO",
            "19": "SAN COSME Y DAMIAN",
            "20": "SAN PEDRO DEL PARANA",
            "21": "SAN RAFAEL DEL PARANA",
            "22": "TRINIDAD",
            "23": "EDELIRA",
            "24": "TOMAS ROMERO PEREIRA",
            "25": "ALTO VERA",
            "26": "LA PAZ",
            "27": "YATYTAY",
            "28": "SAN JUAN DEL PARANA",
            "29": "PIRAPO",
            "30": "ITAPUA POTY",
        }
    },
    "8": {
        "nombre": "MISIONES",
        "distritos": {
            "1": "SAN JUAN BAUTISTA",
            "2": "AYOLAS",
            "3": "SAN IGNACIO",
            "4": "SAN MIGUEL",
            "5": "SAN PATRICIO",
            "6": "SANTA MARIA",
            "7": "SANTA ROSA",
            "8": "SANTIAGO",
            "9": "VILLA FLORIDA",
            "10": "YABEBYRY",
        }
    },
    "9": {
        "nombre": "PARAGUARI",
        "distritos": {
            "1": "PARAGUARI",
            "2": "ACAHAY",
            "3": "CAAPUCU",
            "4": "CABALLERO",
            "5": "CARAPEGUA",
            "6": "ESCOBAR",
            "7": "LA COLMENA",
            "8": "MBUYAPEY",
            "9": "PIRAYU",
            "10": "QUIINDY",
            "11": "QUYQUYHO",
            "12": "SAN ROQUE GONZALEZ",
            "13": "SAPUCAI",
            "14": "TEBICUARYMI",
            "15": "YAGUARON",
            "16": "YBYCUI",
            "17": "YBYTYMI",
        }
    },
    "10": {
        "nombre": "ALTO PARANA",
        "distritos": {
            "1": "CIUDAD DEL ESTE",
            "2": "PRESIDENTE FRANCO",
            "3": "DOMINGO MARTINEZ DE IRALA",
            "4": "DR. JUAN LEON MALLORQUIN",
            "5": "HERNANDARIAS",
            "6": "ITAKYRY",
            "7": "JUAN E. O'LEARY",
            "8": "ÑACUNDAY",
            "9": "YGUAZU",
            "10": "LOS CEDRALES",
            "11": "MINGA GUAZU",
            "12": "SAN CRISTOBAL",
            "13": "SANTA RITA",
            "14": "NARANJAL",
            "15": "SANTA ROSA DEL MONDAY",
            "16": "MINGA PORA",
            "17": "MBARACAYU",
            "18": "SAN ALBERTO",
            "19": "IRUÑA",
            "20": "SANTA FE DEL PARANA",
            "21": "TAVAPY",
            "22": "DR. RAUL PEÑA",
        }
    },
    "11": {
        "nombre": "CENTRAL",
        "distritos": {
            "1": "AREGUA",
            "2": "CAPIATA",
            "3": "FERNANDO DE LA MORA",
            "4": "GUARAMBARE",
            "5": "ITA",
            "6": "ITAUGUA",
            "7": "LAMBARE",
            "8": "LIMPIO",
            "9": "LUQUE",
            "10": "MARIANO ROQUE ALONSO",
            "11": "NUEVA ITALIA",
            "12": "ÑEMBY",
            "13": "SAN ANTONIO",
            "14": "SAN LORENZO",
            "15": "VILLA ELISA",
            "16": "VILLETA",
            "17": "YPACARAI",
            "18": "YPANE",
            "19": "J. AUGUSTO SALDIVAR",
        }
    },
    "12": {
        "nombre": "ÑEEMBUCU",
        "distritos": {
            "1": "PILAR",
            "2": "ALBERDI",
            "3": "CERRITO",
            "4": "DESMOCHADOS",
            "5": "GENERAL JOSE EDUVIGIS DIAZ",
            "6": "GUAZU CUA",
            "7": "HUMAITA",
            "8": "ISLA UMBU",
            "9": "LAURELES",
            "10": "MAYOR JOSE J. MARTINEZ",
            "11": "PASO DE PATRIA",
            "12": "SAN JUAN BAUTISTA DE ÑEEMBUCU",
            "13": "TACUARAS",
            "14": "VILLA FRANCA",
            "15": "VILLALBIN",
            "16": "VILLA OLIVA",
        }
    },
    "13": {
        "nombre": "AMAMBAY",
        "distritos": {
            "1": "PEDRO JUAN CABALLERO",
            "2": "BELLA VISTA NORTE",
            "3": "CAPITAN BADO",
            "4": "KARAPAI",
            "5": "ZANJA PYTA",
        }
    },
    "14": {
        "nombre": "CANINDEYU",
        "distritos": {
            "1": "SALTO DEL GUAIRA",
            "2": "CORPUS CHRISTI",
            "3": "CURUGUATY",
            "4": "VILLA YGATIMI",
            "5": "ITANARA",
            "6": "YPEJHU",
            "7": "FRANCISCO CABALLERO ALVAREZ",
            "8": "KATUETE",
            "9": "LA PALOMA",
            "10": "NUEVA ESPERANZA",
            "11": "YASY KAÑY",
            "12": "YBYRAROBANA",
            "13": "YBY PYTA",
        }
    },
    "15": {
        "nombre": "PRESIDENTE HAYES",
        "distritos": {
            "1": "VILLA HAYES",
            "2": "BENJAMIN ACEVAL",
            "3": "JOSE FALCON",
            "4": "NANAWA",
            "5": "PTO. PINASCO",
            "6": "TTE. 1° MANUEL IRALA FERNANDEZ",
            "7": "GENERAL JOSE MARIA BRUGUEZ",
            "8": "TTE. ESTEBAN MARTINEZ",
        }
    },
    "16": {
        "nombre": "BOQUERON",
        "distritos": {
            "1": "FILADELFIA",
            "2": "LOMA PLATA",
            "3": "MARISCAL ESTIGARRIBIA",
        }
    },
    "17": {
        "nombre": "ALTO PARAGUAY",
        "distritos": {
            "1": "FUERTE OLIMPO",
            "2": "PUERTO CASADO",
            "3": "BAHIA NEGRA",
            "4": "CARMELO PERALTA",
        }
    },
}


def get_departamento(codigo: str) -> dict:
    """Get department info by code."""
    return DEPARTAMENTOS.get(str(codigo), {"nombre": "DESCONOCIDO", "distritos": {}})


def get_distrito(depto_codigo: str, distrito_codigo: str) -> str:
    """Get district name by codes."""
    depto = DEPARTAMENTOS.get(str(depto_codigo), {})
    distritos = depto.get("distritos", {})
    return distritos.get(str(distrito_codigo), "DESCONOCIDO")


def buscar_departamento(nombre: str) -> str:
    """Search department code by name (partial match)."""
    nombre_upper = nombre.upper()
    for codigo, data in DEPARTAMENTOS.items():
        if nombre_upper in data["nombre"]:
            return codigo
    return "11"  # Default: Central
