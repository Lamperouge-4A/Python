from djitellopy import Tello
from inputs import get_gamepad
import cv2
import time
import threading

# Crear objeto Tello
tello = Tello()
tello.connect()
tello.streamon()

# Variable para controlar el video
video_running = True


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
        cv2.putText(frame_rgb, texto_bateria, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

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

# Función para manejar el gamepad
def mapear_valor(valor, min_in, max_in, min_out, max_out):
    """Mapea el valor del joystick a un rango de velocidad."""
    return int((valor - min_in) / (max_in - min_in) * (max_out - min_out) + min_out) 

def controlar_gamepad():
    while True:
        events = get_gamepad()
        for event in events:
            print(event.code, event.state)
        for event in events:
            if event.code == "BTN_SOUTH" and event.state == 1:  # Botón A
                tello.takeoff()
            elif event.code == "BTN_EAST" and event.state == 1:  # Botón B
                tello.land()
            elif event.code == "ABS_Y":  # Joystick izquierdo arriba/abajo (eje Y)
                velocidad = mapear_valor(event.state, -32768, 32767, -100, 100)
                if abs(velocidad) > 10:  # Umbral mínimo
                    if velocidad > 0:
                        tello.move_down(abs(velocidad))
                    else:
                        tello.move_up(abs(velocidad))
            elif event.code == "ABS_X":  # Joystick izquierdo izquierda/derecha (eje X)
                velocidad = mapear_valor(event.state, -32768, 32767, -100, 100)
                if abs(velocidad) > 10:  # Umbral mínimo
                    if velocidad > 0:
                        tello.move_right(abs(velocidad))
                    else:
                        tello.move_left(abs(velocidad))
            
        time.sleep(0.1)  # Reducir carga de la CPU


# Hilo para el control con gamepad
gamepad_thread = threading.Thread(target=controlar_gamepad, daemon=True)
gamepad_thread.start()

try:
    # Mantener el programa corriendo hasta que se cierre la ventana de video
    while video_running:
        time.sleep(1)

except KeyboardInterrupt:
    print("Cerrando el programa...")
    tello.land()
    video_running = False

# Esperar a que el hilo del video termine antes de cerrar el programa
video_thread.join()
