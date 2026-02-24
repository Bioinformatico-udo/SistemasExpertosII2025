"""Reglas taxonómicas para las 11 especies de porcelánidos de Venezuela.

Definición de reglas lógicas para el motor de inferencia (Backward Chaining)
basadas en los datos morfológicos recopilados.

Cada regla valida si un espécimen cumple con las características clave de una especie:
1. Ratios morfométricos (con tolerancia).
2. Rasgos cualitativos (liso/rugoso, robusta/delgada).
3. Escala física (Tamaño absoluto del caparazón).
Incluye información biológica detallada y enlaces a fuentes externas.
"""

def chequear_rango(valor, objetivo, tolerancia=0.12):
    """Verifica si un valor numérico está cerca del objetivo con mayor precisión.

    Args:
        valor: El valor medido en el espécimen.
        objetivo: El valor promedio esperado para la especie.
        tolerancia: Porcentaje de desviación permitido (0.12 = +/- 12%).

    Returns:
        True si el valor está dentro del rango [objetivo - tol, objetivo + tol].
    """
    try:
        v = float(valor)
        o = float(objetivo)
        # Calcula si v está entre el límite inferior y superior
        return (o * (1 - tolerancia)) <= v <= (o * (1 + tolerancia))
    except (ValueError, TypeError):
        return False

def regla_pisidia_brasiliensis():
    """Regla para Pisidia brasiliensis: Pequeño, caparazón liso, quela robusta."""
    return {
        'id': 'R_PIS_BRA',
        'species': 'Pisidia brasiliensis',
        'conditions': [
            lambda r: chequear_rango(r.get('ratio_rostro', 0), 0.26),
            lambda r: chequear_rango(r.get('ratio_quela', 0), 2.25),
            lambda r: chequear_rango(r.get('longitud_caparazon_mm', 0), 3.8), # Talla característica
            lambda r: str(r.get('ornamentacion_caparazon', '')).lower() == 'lisa',
            lambda r: str(r.get('forma_quela', '')).lower() == 'robusta'
        ],
        'justification': 'Tamaño pequeño ~3-4mm, rostro corto, caparazón liso.',
        'info_detallada': 'Habita en aguas someras (0-100m) en ambientes marinos y salobres.',
        'link_especie': 'https://www.marinespecies.org/aphia.php?p=taxdetails&id=425845',
        'threshold': 0.8
    }

def regla_porcellana_sayana():
    """Regla para Porcellana sayana: Caparazón liso, quela delgada, comensal."""
    return {
        'id': 'R_POR_SAY',
        'species': 'Porcellana sayana',
        'conditions': [
            lambda r: chequear_rango(r.get('ratio_rostro', 0), 0.25),
            lambda r: chequear_rango(r.get('ratio_quela', 0), 3.0),
            lambda r: chequear_rango(r.get('longitud_caparazon_mm', 0), 12.0), # Talla característica
            lambda r: str(r.get('ornamentacion_caparazon', '')).lower() == 'lisa',
            lambda r: str(r.get('forma_quela', '')).lower() == 'delgada'
        ],
        'justification': 'Rojizo con manchas, rostro triangular, quelas delgadas.',
        'info_detallada': 'Conocida como cangrejo porcelana manchado, suele vivir de forma comensal con cangrejos ermitaños.',
        'link_especie': 'https://www.marinespecies.org/aphia.php?p=taxdetails&id=421869',
        'threshold': 0.8
    }

def regla_megalobrachium_roseum():
    """Regla para M. roseum: Rugoso, setas presentes."""
    return {
        'id': 'R_MEG_ROS',
        'species': 'Megalobrachium roseum',
        'conditions': [
            lambda r: chequear_rango(r.get('ratio_rostro', 0), 0.30),
            lambda r: chequear_rango(r.get('ratio_quela', 0), 2.2),
            lambda r: chequear_rango(r.get('longitud_caparazon_mm', 0), 5.0), # Talla característica
            lambda r: str(r.get('ornamentacion_caparazon', '')).lower() == 'rugosa',
            lambda r: int(r.get('presencia_setas', 0)) == 1
        ],
        'justification': 'Caparazón rugoso, quelas espinosas y setosas.',
        'info_detallada': 'Originalmente descrita como Porcellana rosea; habita en ambientes marinos y salobres.',
        'link_especie': 'https://www.marinespecies.org/aphia.php?p=taxdetails&id=421868',
        'threshold': 0.8
    }

def regla_megalobrachium_poeyi():
    """Regla para M. poeyi: Similar a roseum pero quela más robusta/aplanada."""
    return {
        'id': 'R_MEG_POE',
        'species': 'Megalobrachium poeyi',
        'conditions': [
            lambda r: chequear_rango(r.get('ratio_rostro', 0), 0.27),
            lambda r: chequear_rango(r.get('ratio_quela', 0), 2.0),
            lambda r: chequear_rango(r.get('longitud_caparazon_mm', 0), 6.5), # Talla característica
            lambda r: str(r.get('ornamentacion_caparazon', '')).lower() == 'rugosa',
            lambda r: str(r.get('forma_quela', '')).lower() == 'robusta',
            lambda r: int(r.get('presencia_setas', 0)) == 1
        ],
        'justification': 'Quelas grandes, aplanadas y setosas.',
        'info_detallada': 'Conocido como cangrejo porcelana de pinzas peludas. Único miembro de su género en ambos lados del istmo de Panamá.',
        'link_especie': 'https://www.marinespecies.org/aphia.php?p=taxdetails&id=421864',
        'threshold': 0.8
    }

def regla_petrolisthes_marginatus():
    """Regla para P. marginatus: Grande, liso."""
    return {
        'id': 'R_PET_MAR',
        'species': 'Petrolisthes marginatus',
        'conditions': [
            lambda r: chequear_rango(r.get('ratio_rostro', 0), 0.23),
            lambda r: chequear_rango(r.get('ratio_quela', 0), 3.0),
            lambda r: chequear_rango(r.get('longitud_caparazon_mm', 0), 15.0), # Talla característica
            lambda r: str(r.get('ornamentacion_caparazon', '')).lower() == 'lisa'
        ],
        'justification': 'Especie grande, caparazón liso.',
        'info_detallada': 'Especie marina de gran tamaño común en el Caribe y las costas de Venezuela.',
        'link_especie': 'https://www.marinespecies.org/aphia.php?p=taxdetails&id=421877',
        'threshold': 0.75
    }

def regla_petrolisthes_galathinus():
    """Regla para P. galathinus: Rugoso (estrías pilosas), complejo."""
    return {
        'id': 'R_PET_GAL',
        'species': 'Petrolisthes galathinus',
        'conditions': [
            lambda r: chequear_rango(r.get('ratio_rostro', 0), 0.25),
            lambda r: chequear_rango(r.get('ratio_quela', 0), 2.8),
            lambda r: chequear_rango(r.get('longitud_caparazon_mm', 0), 12.0), # Talla característica
            lambda r: str(r.get('ornamentacion_caparazon', '')).lower() == 'rugosa'
        ],
        'justification': 'Morfológicamente complejo, caparazón rugoso.',
        'info_detallada': 'Se encuentra frecuentemente asociado a esponjas de barril en arrecifes costeros del Atlántico Occidental.',
        'link_especie': 'https://www.marinespecies.org/aphia.php?p=taxdetails&id=421873',
        'threshold': 0.75
    }

def regla_petrolisthes_armatus():
    """Regla para P. armatus: Verde/marrón, rugoso, quela delgada."""
    return {
        'id': 'R_PET_ARM',
        'species': 'Petrolisthes armatus',
        'conditions': [
            lambda r: chequear_rango(r.get('ratio_rostro', 0), 0.25),
            lambda r: chequear_rango(r.get('ratio_quela', 0), 3.3),
            lambda r: chequear_rango(r.get('longitud_caparazon_mm', 0), 8.0), # Talla característica
            lambda r: str(r.get('ornamentacion_caparazon', '')).lower() == 'rugosa',
            lambda r: str(r.get('forma_quela', '')).lower() == 'delgada'
        ],
        'justification': 'Cangrejo verde, crestas en caparazón, quelas delgadas.',
        'info_detallada': 'Habitante común de manglares y zonas intermareales. Se alimenta filtrando plancton con sus piezas bucales.',
        'link_especie': 'https://www.marinespecies.org/aphia.php?p=taxdetails&id=421870',
        'threshold': 0.8
    }

def regla_petrolisthes_tonsorius():
    """Regla para P. tonsorius: Pequeño, liso, intermareal."""
    return {
        'id': 'R_PET_TON',
        'species': 'Petrolisthes tonsorius',
        'conditions': [
            lambda r: chequear_rango(r.get('ratio_rostro', 0), 0.26),
            lambda r: chequear_rango(r.get('ratio_quela', 0), 2.75),
            lambda r: chequear_rango(r.get('longitud_caparazon_mm', 0), 4.5), # Talla característica
            lambda r: str(r.get('ornamentacion_caparazon', '')).lower() == 'lisa'
        ],
        'justification': 'Intermareal, pequeño, caparazón liso.',
        'info_detallada': 'Habita bajo rocas intermareales en áreas con fuerte movimiento de agua.',
        'link_especie': 'https://www.marinespecies.org/aphia.php?p=taxdetails&id=431835',
        'threshold': 0.75
    }

def regla_petrolisthes_tridentatus():
    """Regla para P. tridentatus: Frente tridentada caracteristica."""
    return {
        'id': 'R_PET_TRI',
        'species': 'Petrolisthes tridentatus',
        'conditions': [
            lambda r: chequear_rango(r.get('ratio_rostro', 0), 0.25),
            lambda r: chequear_rango(r.get('ratio_quela', 0), 3.0),
            lambda r: chequear_rango(r.get('longitud_caparazon_mm', 0), 8.0), # Talla característica
            lambda r: str(r.get('ornamentacion_caparazon', '')).lower() == 'lisa'
        ],
        'justification': 'Aguas someras, frente tridentada inferida.',
        'info_detallada': 'Presente en diversos ambientes marinos y estuarinos de aguas someras.',
        'link_especie': 'https://www.marinespecies.org/aphia.php?p=taxdetails&id=493150',
        'threshold': 0.75
    }

def regla_petrolisthes_jugosus():
    """Regla para P. jugosus: Muy pequeño, colorido."""
    return {
        'id': 'R_PET_JUG',
        'species': 'Petrolisthes jugosus',
        'conditions': [
            lambda r: chequear_rango(r.get('ratio_rostro', 0), 0.23),
            lambda r: chequear_rango(r.get('ratio_quela', 0), 2.5),
            lambda r: chequear_rango(r.get('longitud_caparazon_mm', 0), 2.1), # Talla característica
            lambda r: str(r.get('ornamentacion_caparazon', '')).lower() == 'lisa'
        ],
        'justification': 'Muy pequeño, rojo y blanco, bentónico.',
        'info_detallada': 'Pequeño cangrejo de coloración roja y blanca que habita en fondos rocosos hasta los 190m.',
        'link_especie': 'https://www.marinespecies.org/aphia.php?p=taxdetails&id=421876',
        'threshold': 0.75
    }

def regla_petrolisthes_politus():
    """Regla para P. politus: Liso, brillante, robusto."""
    return {
        'id': 'R_PET_POL',
        'species': 'Petrolisthes politus',
        'conditions': [
            lambda r: chequear_rango(r.get('ratio_rostro', 0), 0.21),
            lambda r: chequear_rango(r.get('ratio_quela', 0), 2.66),
            lambda r: chequear_rango(r.get('longitud_caparazon_mm', 0), 7.0), # Talla característica
            lambda r: str(r.get('ornamentacion_caparazon', '')).lower() == 'lisa'
        ],
        'justification': 'Cangrejo porcelana espalda roja (redback).',
        'info_detallada': 'Conocido como cangrejo porcelana de espalda roja por su llamativa coloración dorsal.',
        'link_especie': 'https://www.marinespecies.org/aphia.php?p=taxdetails&id=421881',
        'threshold': 0.75
    }

def reglas_iniciales():
    """Devuelve la lista de reglas definidas para las 11 especies venezolanas."""
    return [
        regla_pisidia_brasiliensis(),
        regla_porcellana_sayana(),
        regla_megalobrachium_roseum(),
        regla_megalobrachium_poeyi(),
        regla_petrolisthes_marginatus(),
        regla_petrolisthes_galathinus(),
        regla_petrolisthes_armatus(),
        regla_petrolisthes_tonsorius(),
        regla_petrolisthes_tridentatus(),
        regla_petrolisthes_jugosus(),
        regla_petrolisthes_politus()
    ]

def obtener_especies_disponibles() -> list:
    """Devuelve lista de nombres de especies definidas en las reglas.
    
    Returns:
        Lista ordenada alfabéticamente de strings.
    """
    reglas = reglas_iniciales()
    return sorted(list(set([r.get('species', '') for r in reglas if r.get('species')])))
