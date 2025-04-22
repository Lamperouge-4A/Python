import cv2
import numpy as np

cv2.waitKey(1)


def detectar_color(frame):
    # Convertir la imagen a formato HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Definir rangos de colores en HSV
    colores = {
        "Rojo": [(0, 120, 70), (10, 255, 255)],
        "Verde": [(36, 100, 100), (86, 255, 255)],
        "Azul": [(100, 150, 50), (130, 255, 255)],  # Ajuste para evitar confusión con negro
        "Amarillo": [(15, 100, 100), (35, 255, 255)]
    }
    
    for color, (lower, upper) in colores.items():
        lower = np.array(lower, dtype=np.uint8)
        upper = np.array(upper, dtype=np.uint8)
        
        # Crear máscara para el color
        mascara = cv2.inRange(hsv, lower, upper)
        
        # Encontrar contornos
        contornos, _ = cv2.findContours(mascara, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        for contorno in contornos:
            if cv2.contourArea(contorno) > 500:
                x, y, w, h = cv2.boundingRect(contorno)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
                cv2.putText(frame, color, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
    
    return frame

def main():
    cap = cv2.VideoCapture(0)  # Capturar desde la cámara
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = detectar_color(frame)
        cv2.imshow("Detección de Colores", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
