from djitellopy import Tello
import cv2
import time
import threading

# Crear objeto Tello
tello = Tello()

# Conectar al dron
tello.connect()

# Iniciar el Video
tello.streamon()

# Función para mostrar el video en un hilo separado
def mostrar_video():
    while True:
        # Capturar el frame de la cámara
        frame = tello.get_frame_read().frame

        # Corregir el color de BGR a RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Obtener el nivel de batería
        bateria = tello.get_battery()

        # Mostrar el nivel de batería en la esquina superior derecha
        texto_bateria = f"Bateria: {bateria}%"
        cv2.putText(frame_rgb, texto_bateria, (8, 25), cv2.FONT_HERSHEY_PLAIN, 1, (160, 206, 222), 2, cv2.LINE_AA)

        # Mostrar el frame corregido con el nivel de batería
        cv2.imshow("Tello Video Stream", frame_rgb)

        # Salir si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Apagar la transmisión de video y cerrar ventanas
    tello.streamoff()
    cv2.destroyAllWindows()

# Iniciar el hilo para mostrar el video
video_thread = threading.Thread(target=mostrar_video)
video_thread.start()

# Ejecutar las maniobras de vuelo
try:
    # Esperar unos segundos para ver el video antes del despegue
    time.sleep(3)

    
    tello.takeoff ()
    time.sleep(2)
    tello.land()
    time.sleep(1)
    tello.emergency()  

except KeyboardInterrupt:
    # Manejar la interrupción con Ctrl+C
    tello.land()

# Esperar a que el hilo del video termine antes de cerrar el programa
video_thread.join() 