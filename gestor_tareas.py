import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime
import json
import os
import threading
from plyer import notification

# Lista para almacenar las tareas
tareas = []

# Crear la ventana principal de la aplicación
root = tk.Tk()
root.title("Gestión de Tareas Diarias")
root.geometry("600x700")

# Variable global para la fecha seleccionada
fecha_seleccionada = tk.StringVar()
hora_seleccionada = tk.StringVar()  # Para almacenar la hora seleccionada
modo_claro = tk.BooleanVar(value=True)

# Función para configurar el estilo (temas claro y oscuro)
def configurar_estilo(claro=True):
    style = ttk.Style()
    style.theme_use("clam")
    if claro:
        root.configure(bg="#f7f7f7")  # Fondo claro
        style.configure("TButton", background="#4CAF50", foreground="white")
        style.configure("TLabel", background="#f7f7f7", foreground="#333")
        lista_tareas.config(bg="#f9f9f9", fg="#333")
    else:
        root.configure(bg="#333")  # Fondo oscuro
        style.configure("TButton", background="#666", foreground="white")
        style.configure("TLabel", background="#333", foreground="#EEE")
        lista_tareas.config(bg="#444", fg="#FFF")

# Crear el Listbox para las tareas
lista_tareas = tk.Listbox(root, height=10, width=80)
lista_tareas.pack(pady=20)

configurar_estilo()

# Función para abrir el calendario y seleccionar una fecha
def abrir_calendario():
    def seleccionar_fecha():
        fecha_seleccionada.set(calendario.get_date())
        ventana_calendario.destroy()

    ventana_calendario = tk.Toplevel(root)
    ventana_calendario.title("Seleccionar Fecha")
    calendario = Calendar(ventana_calendario, date_pattern="yyyy-mm-dd")
    calendario.pack(pady=10)
    ttk.Button(ventana_calendario, text="Seleccionar", command=seleccionar_fecha).pack(pady=10)

# Función para agregar una tarea
def agregar_tarea():
    descripcion = entry_tarea.get("1.0", tk.END).strip()
    fecha = fecha_seleccionada.get()
    hora = hora_seleccionada.get()
    repeticion = entry_repeticion.get()
    categoria = categoria_seleccionada.get()
    
    if descripcion and fecha and hora:
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
            datetime.strptime(hora, "%H:%M")
            
            tarea = {
                "descripcion": descripcion,
                "fecha": fecha,
                "hora": hora,
                "repeticion": repeticion if repeticion else "No se repite",
                "categoria": categoria
            }
            tareas.append(tarea)
            guardar_tareas()
            notificar_tarea(tarea)
            actualizar_lista()
            entry_tarea.delete("1.0", tk.END)
            fecha_seleccionada.set("")
            hora_seleccionada.set("")
            entry_repeticion.delete(0, tk.END)
            categoria_seleccionada.set("General")
        except ValueError:
            messagebox.showerror("Error", "La fecha debe ser válida y la hora en formato HH:MM.")
    else:
        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios excepto repetición.")

# Función para editar una tarea
def editar_tarea():
    try:
        tarea_seleccionada = lista_tareas.curselection()
        indice = tarea_seleccionada[0]
        tarea = tareas[indice]
        
        entry_tarea.delete("1.0", tk.END)
        entry_tarea.insert("1.0", tarea["descripcion"])
        fecha_seleccionada.set(tarea["fecha"])
        hora_seleccionada.set(tarea["hora"])
        entry_repeticion.delete(0, tk.END)
        entry_repeticion.insert(0, tarea["repeticion"])
        categoria_seleccionada.set(tarea["categoria"])
        
        tareas.pop(indice)
        guardar_tareas()
        actualizar_lista()
    except IndexError:
        messagebox.showwarning("Advertencia", "Por favor, selecciona una tarea para editar.")

# Función para eliminar una tarea
def eliminar_tarea():
    try:
        tarea_seleccionada = lista_tareas.curselection()
        tareas.pop(tarea_seleccionada[0])
        guardar_tareas()
        actualizar_lista()
    except IndexError:
        messagebox.showwarning("Advertencia", "Por favor, selecciona una tarea para eliminar.")

# Función para marcar una tarea como completada
def completar_tarea():
    try:
        tarea_seleccionada = lista_tareas.curselection()
        indice = tarea_seleccionada[0]
        tarea = tareas[indice]
        tarea["descripcion"] += " (Completada)"
        guardar_tareas()
        actualizar_lista()
    except IndexError:
        messagebox.showwarning("Advertencia", "Por favor, selecciona una tarea para completar.")

# Función para alternar el modo oscuro
def alternar_modo():
    modo_claro.set(not modo_claro.get())
    configurar_estilo(claro=modo_claro.get())

# Función para actualizar la lista visual
def actualizar_lista():
    lista_tareas.delete(0, tk.END)
    for tarea in tareas:
        tarea_str = (
            f"[{tarea['categoria']}] {tarea['descripcion'].splitlines()[0]} - "
            f"{tarea['fecha']} {tarea['hora']} - Repite: {tarea['repeticion']}"
        )
        lista_tareas.insert(tk.END, tarea_str)

# Función para guardar las tareas en un archivo JSON
def guardar_tareas():
    with open("tareas.json", "w") as file:
        json.dump(tareas, file)

# Función para cargar las tareas desde un archivo JSON
def cargar_tareas():
    if os.path.exists("tareas.json"):
        with open("tareas.json", "r") as file:
            return json.load(file)
    return []

# Función para notificar sobre la tarea programada
def notificar_tarea(tarea):
    fecha_tarea = datetime.strptime(tarea["fecha"] + " " + tarea["hora"], "%Y-%m-%d %H:%M")
    ahora = datetime.now()

    if fecha_tarea > ahora:
        tiempo_restante = (fecha_tarea - ahora).total_seconds()

        def mostrar_notificacion():
            notification.notify(
                title=f"Tarea: {tarea['descripcion'].splitlines()[0]}",
                message=f"Recuerda: {tarea['descripcion']}",
                timeout=10
            )

        threading.Timer(tiempo_restante, mostrar_notificacion).start()

# Etiqueta de título
titulo = tk.Label(root, text="Gestión de Tareas Diarias", font=("Helvetica", 16))
titulo.pack(pady=10)

# Formulario de entrada para agregar tareas
frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=10)

ttk.Label(frame_inputs, text="Descripción de la tarea:").grid(row=0, column=0, sticky="w", padx=10)
entry_tarea = tk.Text(frame_inputs, height=5, width=40, wrap="word")
entry_tarea.grid(row=0, column=1, padx=10, pady=5)

ttk.Label(frame_inputs, text="Categoría:").grid(row=1, column=0, sticky="w", padx=10)
categoria_seleccionada = tk.StringVar(value="General")
ttk.Combobox(frame_inputs, textvariable=categoria_seleccionada, values=["General", "Trabajo", "Estudio", "Personal"]).grid(row=1, column=1, padx=10, pady=5)

ttk.Label(frame_inputs, text="Repetición:").grid(row=2, column=0, sticky="w", padx=10)
entry_repeticion = ttk.Entry(frame_inputs, width=30)
entry_repeticion.grid(row=2, column=1, padx=10, pady=5)

btn_calendario = ttk.Button(frame_inputs, text="Seleccionar Fecha", command=abrir_calendario)
btn_calendario.grid(row=3, column=0, padx=10, pady=5)

ttk.Label(frame_inputs, text="Hora (HH:MM):").grid(row=3, column=1, sticky="w", padx=10)
hora_seleccionada.set("00:00")
entry_hora = ttk.Entry(frame_inputs, textvariable=hora_seleccionada)
entry_hora.grid(row=4, column=1, padx=10, pady=5)

frame_botones = tk.Frame(root)
frame_botones.pack(pady=10)

ttk.Button(frame_botones, text="Agregar Tarea", command=agregar_tarea).pack(side=tk.LEFT, padx=10)
ttk.Button(frame_botones, text="Editar Tarea", command=editar_tarea).pack(side=tk.LEFT, padx=10)
ttk.Button(frame_botones, text="Eliminar Tarea", command=eliminar_tarea).pack(side=tk.LEFT, padx=10)
ttk.Button(frame_botones, text="Completar Tarea", command=completar_tarea).pack(side=tk.LEFT, padx=10)

btn_modo = ttk.Button(root, text="Alternar Modo Claro/Oscuro", command=alternar_modo)
btn_modo.pack(pady=10)

# Cargar las tareas al iniciar
tareas = cargar_tareas()
actualizar_lista()

root.mainloop()
