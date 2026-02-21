"""
Script para reconstruir el árbol dicotómico completo en la DB.
Cubre todas las especies: Munida (4) + Munidopsis (6) + Munidopsis sp.
"""
import sqlite3

DB_NAME = 'crabs.db'

# Mapeo de IDs de especies conocidas en la DB
# Verificar IDs reales: 22=constricta, 23=evermanni, 24=flinti, 25=forceps,
#                       26=alaminos,  27=brevimanus, 29=erinaceus, 30=longimanus
#                       31=platirostris, 32=polita, 38=Munidopsis sp.

SPECIES_IDS = {
    'constricta':   22,
    'evermanni':    23,
    'flinti':       24,
    'forceps':      25,
    'alaminos':     26,
    'brevimanus':   27,
    'erinaceus':    29,
    'longimanus':   30,
    'platirostris': 31,
    'polita':       32,
    'sp':           38,
}

KEY_NODES = [
    (1,  "¿El caparazón tiene líneas transversales bien marcadas (visible patrón de bandas)?"),
    (2,  "¿Tiene espinas en el margen posterior del caparazón?"),
    (3,  "¿La espina antenular EXTERNA terminal es marcadamente más larga que la interna?"),
    (4,  "¿Las espinas supraoculares sobrepasan o llegan hasta la córnea?"),
    (5,  "¿El tercer maxilípedo tiene una espina ventral fuerte?"),
    (6,  "¿El caparazón tiene espinas cónicas prominentes (no solo tubérculos)?"),
    (7,  "¿El pedúnculo ocular tiene espinas?"),
    (8,  "¿La región gástrica del caparazón tiene espinas o tubérculos agudos?"),
    (9,  "¿El abdomen tiene espinas (no solo tubérculos redondeados)?"),
    (10, "¿El caparazón tiene al menos un par de espinas gástricas (epigástricas/protogástricas)?"),
    (11, "¿La región cardíaca del caparazón tiene espinas?"),
    (12, "¿Los quelípedos son muy largos (3 a 4 veces la longitud del caparazón)?"),
    (13, "¿El caparazón y abdomen están completamente lisos (sin espinas ni tubérculos)?"),
]

# (node_id, option_text, next_node_id, species_id)
KEY_OPTIONS = [
    # Nodo 1: ¿Líneas transversales en caparazón?
    (1, "SÍ — líneas transversales bien marcadas (género Munida)",    2,    None),
    (1, "NO — sin líneas o muy tenues (género Munidopsis)",           6,    None),

    # Nodo 2: ¿Espinas en margen posterior?
    (2, "SÍ — margen posterior con espinas",  3,    None),
    (2, "NO — margen posterior sin espinas",  4,    None),

    # Nodo 3: ¿Espina antenular externa marcadamente más larga?
    (3, "SÍ — espina EXTERNA claramente más larga",  11,  None),
    (3, "NO — espina INTERNA igual o más larga",     5,   None),

    # Nodo 4: ¿Espinas supraoculares alcanzan la córnea?
    (4, "SÍ — sobrepasan o alcanzan la córnea",  None, SPECIES_IDS['evermanni']),
    (4, "NO — no alcanzan la córnea",            None, SPECIES_IDS['flinti']),

    # Nodo 5: ¿Espina ventral fuerte en tercer maxilípedo?
    (5, "SÍ — espina ventral fuerte en 3er maxilípedo",  None, SPECIES_IDS['flinti']),
    (5, "NO — sin espina ventral distinguible",          None, SPECIES_IDS['evermanni']),

    # Nodo 6: ¿Espinas cónicas en caparazón?
    (6, "SÍ — espinas cónicas prominentes en caparazón",  7,    None),
    (6, "NO — sin espinas agudas (tubérculos o liso)",    10,   None),

    # Nodo 7: ¿Pedúnculo ocular con espinas?
    (7, "SÍ — pedúnculo ocular armado con espinas",    None, SPECIES_IDS['alaminos']),
    (7, "NO — pedúnculo ocular sin espinas",           8,    None),

    # Nodo 8: ¿Región gástrica con espinas/tubérculos agudos?
    (8, "Un PAR de espinas/tubérculos gástricos prominentes",  None, SPECIES_IDS['brevimanus']),
    (8, "MÚLTIPLES espinas gástricas y cardíacas",             None, SPECIES_IDS['erinaceus']),
    (8, "Espina postantenal larga, sin espinas gástricas evidentes", None, SPECIES_IDS['platirostris']),

    # Nodo 9: ¿Abdomen con espinas?
    (9, "SÍ — abdomen con espinas claras",   12,  None),
    (9, "NO — abdomen liso o con tubérculos", 13,  None),

    # Nodo 10: ¿Espinas gástricas (con caparazón sin espinas cónicas)?
    (10, "SÍ — al menos un par de espinas/tubérculos en región gástrica", 9, None),
    (10, "NO — caparazón y abdomen sin espinas ni tubérculos",            None, SPECIES_IDS['polita']),

    # Nodo 11: ¿Región cardíaca con espinas? (diferencia constricta vs forceps)
    (11, "SÍ — región cardíaca con espinas",   None, SPECIES_IDS['constricta']),
    (11, "NO — región cardíaca sin espinas (quelípedos muy robustos)", None, SPECIES_IDS['forceps']),

    # Nodo 12: ¿Quelípedos muy largos (3-4x LC)?
    (12, "SÍ — quelípedos muy largos (3–4× longitud caparazón)",  None, SPECIES_IDS['longimanus']),
    (12, "NO — quelípedos moderados",                             None, SPECIES_IDS['platirostris']),

    # Nodo 13: ¿Completamente liso?
    (13, "SÍ — caparazón y abdomen completamente lisos",   None, SPECIES_IDS['polita']),
    (13, "NO — algún tubérculo o carácter distintivo",    None, SPECIES_IDS['sp']),
]

def rebuild_key():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Limpiar tablas
    c.execute("DELETE FROM key_options")
    c.execute("DELETE FROM key_nodes")
    c.execute("UPDATE sqlite_sequence SET seq=0 WHERE name='key_options'")
    
    # Insertar nodos
    c.executemany("INSERT INTO key_nodes (id, question) VALUES (?, ?)", KEY_NODES)
    
    # Insertar opciones
    c.executemany(
        "INSERT INTO key_options (node_id, option_text, next_node_id, species_id) VALUES (?, ?, ?, ?)",
        KEY_OPTIONS
    )
    
    conn.commit()
    conn.close()
    print(f"✓ {len(KEY_NODES)} nodos y {len(KEY_OPTIONS)} opciones insertados correctamente.")
    
    # Verificación rápida
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM key_nodes")
    print(f"  key_nodes: {c.fetchone()[0]} filas")
    c.execute("SELECT COUNT(*) FROM key_options")
    print(f"  key_options: {c.fetchone()[0]} filas")
    conn.close()

if __name__ == "__main__":
    rebuild_key()
