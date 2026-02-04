""" ************************** 
    ***     IMAGE HELPER     *** 
    ************************** """
# Este archivo contiene la clase ImageHelper que se encarga de gestionar el procesamiento de imágenes.

# --- Importaciones ---
import cv2
import numpy as np
import os

# --- Clase principal ---
class ImageHelper:
    @staticmethod # Metodo estatico que sirve para procesar la imagen y detectar rasgos taxonómicos básicos funciona con OpenCV
    # @staticmethod es un decorador que permite que un metodo sea llamado sin necesidad de crear una instancia de la clase
    
    # Función que procesa la imagen y detecta rasgos taxonómicos básicos
    def process_image(image_path):
        """
        Analiza la imagen para detectar rasgos taxonómicos básicos.
        Extrae contornos y dimensiones del espécimen.
        """
        try:
            img = cv2.imread(image_path)
            if img is None: return None
            
            # 1. Preprocesamiento
            # Reducir ruido y convertir a escala de grises
            blur = cv2.GaussianBlur(img, (5, 5), 0)
            gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
            
            # 2. Segmentación (Canny edge detection o Thresholding)
            # Usamos Otsu's thresholding para separar al espécimen del fondo
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            
            # 3. Detección de Contornos
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if not contours:
                return {"status": "no_specimen_detected"}
                
            # Tomar el contorno más grande (asumimos que es el espécimen)
            c = max(contours, key=cv2.contourArea) if len(contours) > 0 else None
            if c is None: return None
            
            # 4. Análisis de Forma (Conceptualización Taxonómica)
            x, y, w, h = cv2.boundingRect(c)
            aspect_ratio = float(w)/h
            
            # Clasificar forma
            shape_type = "ovalado" if aspect_ratio < 0.8 else "subcilindrico"
            
            # --- NUEVO: Dibujar resaltado visual ---
            processed_img = img.copy()
            # Dibujar contorno en verde cian
            cv2.drawContours(processed_img, [c], -1, (255, 255, 0), 2)
            # Dibujar cuadro delimitador
            cv2.rectangle(processed_img, (x, y), (x + w, y + h), (0, 255, 255), 2)
            # Añadir etiqueta (Ajuste dinámico para que no se corte arriba)
            text_y = y - 10 if y > 30 else y + 25
            cv2.putText(processed_img, f"IA: {shape_type.upper()}", (x, text_y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            
            # Guardar visualización temporal
            temp_path = os.path.join("assets", "temp_detection.png")
            cv2.imwrite(temp_path, processed_img)
            
            return {
                "status": "success",
                "aspect_ratio": round(aspect_ratio, 2),
                "detected_shape": shape_type,
                "bbox": (x, y, w, h),
                "processed_image": temp_path
            }
        except Exception as e:
            print(f"Error en ImageHelper: {e}")
            return None

# Instancia global
image_helper = ImageHelper()
