BASE_DE_CONOCIMIENTO = {
  "pregunta": "Comencemos por la parte posterior: ¿Qué proporción guarda el telson (la pieza final de la cola) respecto al caparazón?",
  "imagen": "imagenes/telson_largo.png",
  "opciones": {
    "Largo (Al menos la mitad del caparazón)": {
      "nota": "Esta proporción es característica de la familia Hippidae [1].",
      "pregunta": "Ahora observa la parte frontal: ¿Cómo es la longitud del flagelo antenal comparado con las anténulas?",
      "imagen": "imagenes/flagelo.jpg",
      "opciones": {
        "Es más corto": {
          "nota": "Has identificado al género Hippa. En el Caribe, este género cuenta con una única especie registrada [2, 3].",
          "resultado": "Hippa testudinaria"
        },
        "Es mucho más largo": {
          "nota": "Estas antenas largas y setosas indican que estamos ante el género Emerita [2, 4].",
          "pregunta": "Examine con cuidado la punta (dáctilo) de la primera pata o pereiópodo:",
          "imagen": "imagenes/dactilo_redondeado.jpg",
          "opciones": {
            "Punta redondeada": {
              "nota": "Este rasgo suele identificar a E. brasiliensis, aunque su presencia en Venezuela está bajo debate molecular reciente [5-7].",
              "resultado": "Emerita brasiliensis"
            },
            "Punta aguda": {
              "nota": "La forma aguda es diagnóstica para esta especie, que suele habitar junto a otras en nuestras costas [5, 8, 9].",
              "resultado": "Emerita portoricensis"
            }
          }
        }
      }
    },
    "Corto (Mucho menos de la mitad del caparazón)": {
      "nota": "Este rasgo, junto a dáctilos en forma de hoz, define a la familia Albuneidae [10].",
      "pregunta": "Mira el borde delantero del caparazón: ¿Presenta espinas que lo hacen lucir aserrado?",
      "imagen": "imagenes/caparazon_aserrado.jpg",
      "opciones": {
        "Sí, es aserrado": {
          "nota": "La presencia de 'sierra' frontal define al género Albunea [11].",
          "pregunta": "Revisemos la cuarta pata: ¿Cómo describirías la curvatura o depresión en su margen posterior?",
          "imagen": "imagenes/dactilo_depresion.jpg",
          "opciones": {
            "Es una caída o depresión brusca": {
              "nota": "¡Excelente hallazgo! Esta especie es una nueva adición al inventario de Venezuela, reportada en la Isla La Tortuga [12-14].",
              "resultado": "Albunea catherinae"
            },
            "Es una caída suave o gradual": {
              "nota": "Esta especie es común en el Caribe y puede habitar hasta los 101 m de profundidad [13, 15].",
              "resultado": "Albunea paretii"
            }
          }
        },
        "No, el margen es liso (no aserrado)": {
          "nota": "El margen liso es propio del género Lepidopa [11].",
          "pregunta": "¿Qué forma predominante notas en los pedúnculos oculares (los ojos)?",
          "imagen": "imagenes/ojos_subovalados.jpg",
          "opciones": {
            "Tienen forma subovalada": {
              "nota": "Esta especie es muy parecida a L. luciae, pero se distingue por el talón agudo en sus patas [16-18].",
              "resultado": "Lepidopa venusta"
            },
            "Tienen forma subrectangular (más cuadraditos)": {
              "nota": "Es la especie de Lepidopa más frecuente y ampliamente distribuida en las costas venezolanas [16, 19].",
              "resultado": "Lepidopa richmondi"
            }
          }
        }
      }
    }
  }
}