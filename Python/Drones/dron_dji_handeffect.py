import cv2
import time
from djitellopy import Tello
import threading
import mediapipe as mp

# Definimos la variable tello y la conectamos
hi5 = Tello()
hi5.connect()

# Iniciamos la cámara
hi5.streamon()

# Configuración de MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Función para mostrar el video con el mapeo de manos
def mostrar_video():
    while True:
        frame = hi5.get_frame_read().frame
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.imshow("Tello Video", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('t'):  # Despegar
            print("Despegando...")
            hi5.takeoff()
        elif key == ord('w'):  # Subir 30 cm
            print("Subiendo 30 cm...")
            hi5.move_up(30)
        elif key == ord('s'):  # Bajar 30 cm
            print("Bajando 30 cm...")
            hi5.move_down(30)
        elif key == ord('q'):  # Salir del programa
            print("Cerrando...")
            break

    cv2.destroyAllWindows()
    hi5.streamoff()
    hi5.land()  # Aterriza antes de salir

# Iniciar el video en un hilo diferente para no bloquear el programa
video_thread = threading.Thread(target=mostrar_video)
video_thread.start()
