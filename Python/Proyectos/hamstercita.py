import pyautogui
import time
import webbrowser

# Configura aquí
contacto = "hamstercita <3"  # Cambia esto por el nombre exacto
mensaje = " Holis! Estoy trabajando amor, pero no olvides que te amo." 
intervalo = 900  # segundos entre mensajes (900s = 15 minutos)

# Abrir WhatsApp Web en el navegador
webbrowser.open("https://web.whatsapp.com/")
print("Abriendo WhatsApp Web... Escanea el código QR si es necesario.")
time.sleep(15)  # Espera a que cargue WhatsApp Web completamente

# Buscar el contacto o grupo
pyautogui.write(contacto)
time.sleep(1)
pyautogui.press("enter")
time.sleep(2)

# Enviar el primer mensaje inmediatamente
pyautogui.write(mensaje)
pyautogui.press("enter")
print(f"[Inicial] Mensaje enviado a {contacto}")

# Esperar y continuar enviando el mismo mensaje cada 15 minutos
while True:
    time.sleep(intervalo)
    pyautogui.write(mensaje)
    pyautogui.press("enter")
    print(f"[Automático] Mensaje enviado a {contacto}")
