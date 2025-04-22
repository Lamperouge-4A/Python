import tkinter as tk
from tkinter import scrolledtext
import difflib
import random
from module_responses import respuestas


def buscar_similar(pregunta, base_respuestas):
    coincidencia = difflib.get_close_matches(pregunta, base_respuestas.keys(), n=1, cutoff=0.6)
    if coincidencia:
        return base_respuestas[coincidencia[0]]
    return "Lo siento, no entiendo tu pregunta."


# Función para manejar la interacción
def procesar_entrada(event=None):  # Se añade `event` para capturar la tecla Enter
    entrada = entrada_usuario.get().strip()
    if not entrada:
        agregar_a_chat("Schrödinger: Por favor, escribe algo.")
        return

    if entrada.lower() == "salir":
        ventana.destroy()
        return

    # Responder según las entradas
    respuesta = buscar_similar(entrada, respuestas)

    agregar_a_chat(f"Tú: {entrada}")
    agregar_a_chat(f"Schrödinger: {respuesta}")
    entrada_usuario.delete(0, tk.END)


# Función para agregar texto al área de chat
def agregar_a_chat(mensaje):
    area_chat.configure(state="normal")
    area_chat.insert(tk.END, mensaje + "\n")
    area_chat.configure(state="disabled")
    area_chat.see(tk.END)


# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Schrödinger Chatbot")
ventana.geometry("500x600")
ventana.configure(bg="#f5f5f5")  # Fondo pastel claro

# Estilo de colores
color_fondo = "#f5f5f5"  # Fondo general
color_area_chat = "#e8f0f2"  # Fondo del área de chat
color_borde = "#c5dedd"  # Color del borde
color_boton = "#ace7ef"  # Fondo del botón
color_texto_boton = "#007991"  # Texto del botón

# Área de chat
area_chat = scrolledtext.ScrolledText(
    ventana, wrap=tk.WORD, state="disabled", font=("Arial", 12), bg=color_area_chat, fg="#003d5b", bd=1, relief="solid"
)
area_chat.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Mostrar el mensaje de bienvenida en el área de chat
agregar_a_chat("//Escribe 'salir' para cerrar el programa.")

# Campo de entrada de texto
entrada_usuario = tk.Entry(
    ventana, font=("Arial", 14), bg="white", fg="#003d5b", bd=2, relief="solid", highlightbackground=color_borde
)
entrada_usuario.pack(padx=10, pady=(0, 10), fill=tk.X)

# Botón para enviar
boton_enviar = tk.Button(
    ventana, text="Enviar", command=procesar_entrada, font=("Arial", 14), bg=color_boton, fg=color_texto_boton, bd=0
)
boton_enviar.pack(padx=10, pady=10)

# Vincular la tecla Enter al campo de entrada
ventana.bind("<Return>", procesar_entrada)

# Ejecutar la ventana principal
ventana.mainloop()
