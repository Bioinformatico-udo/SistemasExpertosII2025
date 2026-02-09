BASE_DE_CONOCIMIENTO = {
    "pregunta": "Comencemos por la parte posterior: ¿Qué proporción guarda el telson (la pieza final de la cola) respecto al caparazón?",
    "imagen": "imagenes/telson.png",
    "opciones": {
        "B - Largo (Al menos la mitad del caparazón)": {
            "nota": "Esta proporción es característica de la familia Hippidae.",
            "pregunta": "Ahora observa la parte frontal: ¿Cómo es la longitud del flagelo antenal comparado con las anténulas?",
            "imagen": "imagenes/flagelo.png",
            "opciones": {
                "A - Es más corto que las anténulas": {
                    "nota": "Has identificado al género Hippa. En el Caribe, este género cuenta con una única especie registrada.",
                    "resultado": "Hippa testudinaria",
                    "imagen": "imagenes/hippa_testudinaria.jpeg"
                },
                "B - Es mucho más largo que las anténulas": {
                    "nota": "Estas antenas largas y setosas indican que estamos ante el género Emerita.",
                    "pregunta": "Examine con cuidado la punta (dáctilo) de la primera pata o pereiópodo:",
                    "imagen": "imagenes/dactilo_emerita.png",
                    "opciones": {
                        "A - Punta redondeada": {
                            "nota": "Este rasgo suele identificar a E. brasiliensis, aunque su presencia en Venezuela está bajo debate molecular reciente.",
                            "resultado": "Emerita brasiliensis"
                            ,
                            "imagen": "imagenes/emerita_brasiliensis.jpg"
                        },
                        "B - Punta aguda": {
                            "nota": "La forma aguda es diagnóstica para esta especie, que suele habitar junto a otras en nuestras costas.",
                            "resultado": "Emerita portoricensis"
                            ,
                            "imagen": "imagenes/emerita_portoricensis.jpg"
                        }
                    }
                }
            }
        },
        "A - Corto (Mucho menos de la mitad del caparazón)": {
            "nota": "Este rasgo, junto a dáctilos en forma de hoz, define a la familia Albuneidae.",
            "pregunta": "Mira el borde delantero del caparazón: ¿Presenta espinas que lo hacen lucir aserrado?",
            "imagen": "imagenes/caparazon_albuneidae.png",
            "opciones": {
                "A - Sí, el margen es aserrado": {
                    "nota": "La presencia de 'sierra' frontal y ojos subtriangulares define al género Albunea.",
                    "pregunta": "Revisemos la cuarta pata: ¿Cómo describirías la curvatura o depresión en su margen posterior?",
                    "imagen": "imagenes/dactilo_albunea.png",
                    "opciones": {
                        "A - Es una caída o depresión brusca": {
                            "nota": "¡Excelente hallazgo! Esta especie es una nueva adición al inventario de Venezuela, reportada en la Isla La Tortuga.",
                            "resultado": "Albunea catherinae"
                            ,
                            "imagen": "imagenes/Albunea_catherinae.jpg"
                        },
                        "B - Es una caída suave o gradual": {
                            "nota": "Esta especie es común en el Caribe y puede habitar hasta los 101 m de profundidad.",
                            "resultado": "Albunea paretii"
                            ,
                            "imagen": "imagenes/Albunea_paretii.jpg"
                        }
                    }
                },
                "B - No, el margen es liso (no aserrado)": {
                    "nota": "El margen liso es propio del género Lepidopa.",
                    "pregunta": "¿Qué forma predominante notas en los pedúnculos oculares (los ojos)?",
                    "imagen": "imagenes/ojos_lepidopa.png",
                    "opciones": {
                        "A - Tienen forma subovalada": {
                            "nota": "Esta especie es muy parecida a L. luciae, pero se distingue por el talón agudo en sus patas.",
                            "resultado": "Lepidopa venusta"
                            ,
                            "imagen": "imagenes/Ledidopa_venusta.jpeg"
                        },
                        "B - Tienen forma subrectangular (más cuadraditos)": {
                            "nota": "Es la especie de Lepidopa más frecuente y ampliamente distribuida en las costas venezolanas.",
                            "resultado": "Lepidopa richmondi"
                            ,
                            "imagen": "imagenes/ledidopa_richmondi.jpg"
                        }
                    }
                }
            }
        }
    }
}