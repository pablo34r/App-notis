import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import json
import os

# Archivo para almacenar usuarios
ARCHIVO_USUARIOS = "usuarios.json"

# Verificar si el archivo de usuarios existe
if not os.path.exists(ARCHIVO_USUARIOS):
    with open(ARCHIVO_USUARIOS, "w") as file:
        json.dump({}, file)

# Función para cargar usuarios
def cargar_usuarios():
    with open(ARCHIVO_USUARIOS, "r") as file:
        return json.load(file)

# Función para guardar usuarios
def guardar_usuarios(usuarios):
    with open(ARCHIVO_USUARIOS, "w") as file:
        json.dump(usuarios, file)

# Función para centrar la ventana
def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

# Interfaz de registro
def registrar_usuario():
    def registrar():
        username = entry_usuario.get()
        password = entry_contraseña.get()

        if username and password:
            usuarios = cargar_usuarios()
            if username in usuarios:
                messagebox.showerror("Error", "El usuario ya existe.")
            else:
                usuarios[username] = password
                guardar_usuarios(usuarios)
                messagebox.showinfo("Éxito", "Usuario registrado con éxito.")
                ventana_registro.destroy()
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

    ventana_registro = tk.Toplevel()
    ventana_registro.title("Registrar Usuario")
    centrar_ventana(ventana_registro, 400, 300)  # Tamaño más grande y centrado

    ttk.Label(ventana_registro, text="Usuario:", font=("Arial", 14)).pack(pady=10)
    entry_usuario = ttk.Entry(ventana_registro, font=("Arial", 14))
    entry_usuario.pack(pady=10)

    ttk.Label(ventana_registro, text="Contraseña:", font=("Arial", 14)).pack(pady=10)
    entry_contraseña = ttk.Entry(ventana_registro, show="*", font=("Arial", 14))
    entry_contraseña.pack(pady=10)

    ttk.Button(ventana_registro, text="Registrar", command=registrar, style="TButton").pack(pady=20)

# Interfaz de login
def login():
    def iniciar_sesion():
        username = entry_usuario.get()
        password = entry_contraseña.get()

        usuarios = cargar_usuarios()
        if username in usuarios and usuarios[username] == password:
            messagebox.showinfo("Éxito", f"Bienvenido {username}!")
            ventana_login.destroy()
            subprocess.Popen(["python", "gestor_tareas.py"])  # Abre el archivo gestor_tareas.py
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    ventana_login = tk.Tk()
    ventana_login.title("Login")
    centrar_ventana(ventana_login, 400, 300)  # Tamaño más grande y centrado

    ttk.Label(ventana_login, text="Usuario:", font=("Arial", 14)).pack(pady=10)
    entry_usuario = ttk.Entry(ventana_login, font=("Arial", 14))
    entry_usuario.pack(pady=10)

    ttk.Label(ventana_login, text="Contraseña:", font=("Arial", 14)).pack(pady=10)
    entry_contraseña = ttk.Entry(ventana_login, show="*", font=("Arial", 14))
    entry_contraseña.pack(pady=10)

    ttk.Button(ventana_login, text="Iniciar Sesión", command=iniciar_sesion, style="TButton").pack(pady=20)
    ttk.Button(ventana_login, text="Registrarse", command=registrar_usuario, style="TButton").pack(pady=10)

    ventana_login.mainloop()

# Ejecutar la interfaz de login al inicio
login()
