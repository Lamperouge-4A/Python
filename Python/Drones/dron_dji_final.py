from djitellopy import Tello
from inputs import get_gamepad
import threading
import time

# Crear una instancia del dron
tello = Tello()
tello.connect()

# Velocidad base
SPEED = 50

# Variables para controlar el dron
yaw, throttle, roll, pitch = 0, 0, 0, 0
flying = False  # Estado de vuelo

# Función para manejar el control del mando Xbox
def handle_gamepad():
    global yaw, throttle, roll, pitch, flying
    last_event_time = time.time()
    
    try:
        while True:
            events = get_gamepad()
            if events:
                last_event_time = time.time()
                for event in events:
                    # Joystick izquierdo (adelante/atrás y lateral)
                    if event.code == "ABS_Y":
                        pitch = int(-SPEED * (event.state / 32767.0)) if abs(event.state) > 2000 else 0
                    elif event.code == "ABS_X":
                        roll = int(SPEED * (event.state / 32767.0)) if abs(event.state) > 2000 else 0
                    
                    # Joystick derecho (subir/bajar)
                    elif event.code == "ABS_RY":
                        throttle = int(-SPEED * (event.state / 32767.0)) if abs(event.state) > 2000 else 0
                    
                    # Gatillos (rotar el dron)
                    elif event.code == "ABS_Z":  # Gatillo izquierdo
                        yaw = int(-SPEED * (event.state / 255.0)) if event.state > 10 else 0
                    elif event.code == "ABS_RZ":  # Gatillo derecho
                        yaw = int(SPEED * (event.state / 255.0)) if event.state > 10 else 0
                    
                    # Botón "A" para despegar/aterrizar (con confirmación de estado)
                    elif event.code == "BTN_SOUTH" and event.state == 1:
                        if not flying:
                            print("Despegando...")
                            tello.takeoff()
                            flying = True
                        else:
                            print("Aterrizando...")
                            tello.land()
                            flying = False
                    
                    # Botón "B" para detener el dron
                    elif event.code == "BTN_EAST" and event.state == 1:
                        print("Deteniendo dron...")
                        roll, pitch, throttle, yaw = 0, 0, 0, 0
                        tello.send_rc_control(0, 0, 0, 0)
                    
                    # Botón LB para retroceder y RB para avanzar (al soltar, restablece)
                    elif event.code == "BTN_TL":
                        pitch = -SPEED if event.state == 1 else 0
                    elif event.code == "BTN_TR":
                        pitch = SPEED if event.state == 1 else 0
            
            # Si no se reciben eventos en 2 segundos, detener el movimiento
            if time.time() - last_event_time > 2:
                yaw, throttle, roll, pitch = 0, 0, 0, 0
            
            time.sleep(0.01)
    except Exception as e:
        print(f"Error en el control del gamepad: {e}")

# Función para monitorear batería y señal Wi-Fi
def monitor_status():
    try:
        while True:
            battery = tello.get_battery()
            wifi_signal = tello.query_wifi_signal_noise_ratio()  # Consulta la señal Wi-Fi
            print(f"🪫 Batería: {battery}% | 📶 Señal Wi-Fi: {wifi_signal} dB")
            time.sleep(3)  # Consulta cada 5 segundos
    except Exception as e:
        print(f"Error en el monitoreo de batería/señal Wi-Fi: {e}")

# Iniciar los hilos
gamepad_thread = threading.Thread(target=handle_gamepad, daemon=True)
status_thread = threading.Thread(target=monitor_status, daemon=True)

gamepad_thread.start()
status_thread.start()

# Bucle para enviar comandos al dron
try:
    while True:
        # Filtrar valores bajos para evitar fluctuaciones
        yaw = yaw if abs(yaw) > 5 else 0
        throttle = throttle if abs(throttle) > 5 else 0
        roll = roll if abs(roll) > 5 else 0
        pitch = pitch if abs(pitch) > 5 else 0
        
        tello.send_rc_control(roll, pitch, throttle, yaw)
        time.sleep(0.05)  # Ajuste del tiempo de respuesta
except KeyboardInterrupt:
    tello.land()
    print("Dron aterrizando...")
