import tkinter as tk
from tkinter import messagebox
import sqlite3

def actualizar_total(año, mes):
    # Conectar a la base de datos
    conn = sqlite3.connect('datos.db')
    cursor = conn.cursor()

    # Verificar si el registro existe
    cursor.execute('''
        SELECT COUNT(*) FROM registros WHERE ano = ? AND mes = ?
    ''', (año, mes))

    if cursor.fetchone()[0] == 0:
        messagebox.showwarning("Advertencia", f"No existe registro para {año}-{mes}.")
        conn.close()
        return

    # Calcular el total (sumando ingresos y restando gastos)
    cursor.execute('''
        SELECT COALESCE(SUM(i.importe), 0), COALESCE(SUM(g.importe), 0)
        FROM registros r
        LEFT JOIN ingresos i ON r.id = i.registro_id
        LEFT JOIN gastos g ON r.id = g.registro_id
        WHERE r.ano = ? AND r.mes = ?
    ''', (año, mes))

    ingresos_totales, gastos_totales = cursor.fetchone()  # Obtiene los totales de ingresos y gastos

    # Calculamos el total como ingresos - gastos
    total = ingresos_totales - gastos_totales

    # Actualizar el campo total en la tabla registros
    cursor.execute('''
        UPDATE registros
        SET total = ?
        WHERE ano = ? AND mes = ?
    ''', (total, año, mes))

    conn.commit()
    conn.close()


def guardar_gasto(id_registro, nombre, importe, año, mes):
    conn = sqlite3.connect('datos.db')
    cursor = conn.cursor()

    # Insertar el gasto en la base de datos
    cursor.execute('''
        INSERT INTO gastos (nombre, importe, registro_id)
        VALUES (?, ?, ?)
    ''', (nombre, importe, id_registro))

    conn.commit()
    conn.close()

    # Actualizar el total en la tabla registros
    actualizar_total(año, mes)

    messagebox.showinfo("Éxito", "Gasto guardado exitosamente.")

def guardar_ingreso(id_registro, nombre, importe, año, mes):
    conn = sqlite3.connect('datos.db')
    cursor = conn.cursor()

    # Insertar el ingreso en la base de datos
    cursor.execute('''
        INSERT INTO ingresos (nombre, importe, registro_id)
        VALUES (?, ?, ?)
    ''', (nombre, importe, id_registro))

    conn.commit()
    conn.close()

    # Actualizar el total en la tabla registros
    actualizar_total(año, mes)

    messagebox.showinfo("Éxito", "Ingreso guardado exitosamente.")

def ventana_formulario(id, año, mes):
    ventana = tk.Toplevel()
    ventana.title("Año y Mes")
    ventana.geometry("650x600")

    # Título
    tk.Label(ventana, text="Formulario para Ingresos y Gastos", font=("Arial", 14, "bold")).pack(pady=10)

    # No hay campo de ID de registro, se usa el ID pasado como parámetro

    # Parte de Ingresos
    ingresos_frame = tk.LabelFrame(ventana, text="Ingresos", font=("Arial", 12), padx=20, pady=20)
    ingresos_frame.pack(fill="both", expand=True, padx=10, pady=5)

    tk.Label(ingresos_frame, text="Concepto de ingreso", font=("Arial", 10)).pack(pady=5)
    ingreso_nombre = tk.Entry(ingresos_frame, font=("Arial", 10))
    ingreso_nombre.pack(pady=5)

    tk.Label(ingresos_frame, text="Importe", font=("Arial", 10)).pack(pady=5)
    ingreso_importe = tk.Entry(ingresos_frame, font=("Arial", 10))
    ingreso_importe.pack(pady=5)

    def insertar_ingreso():
        nombre = ingreso_nombre.get()
        try:
            importe = float(ingreso_importe.get())
            if nombre and importe > 0:
                guardar_ingreso(id, nombre, importe, año, mes)
            else:
                messagebox.showwarning("Advertencia", "El importe debe ser mayor que 0.")
        except ValueError:
            messagebox.showwarning("Advertencia", "El importe debe ser un número válido.")

    tk.Button(ingresos_frame, text="Insertar Ingreso", command=insertar_ingreso, font=("Arial", 12)).pack(pady=10)

    # Parte de Gastos
    gastos_frame = tk.LabelFrame(ventana, text="Gastos", font=("Arial", 12), padx=20, pady=20)
    gastos_frame.pack(fill="both", expand=True, padx=10, pady=5)

    tk.Label(gastos_frame, text="Concepto de gasto", font=("Arial", 10)).pack(pady=5)
    gasto_nombre = tk.Entry(gastos_frame, font=("Arial", 10))
    gasto_nombre.pack(pady=5)

    tk.Label(gastos_frame, text="Importe", font=("Arial", 10)).pack(pady=5)
    gasto_importe = tk.Entry(gastos_frame, font=("Arial", 10))
    gasto_importe.pack(pady=5)

    def insertar_gasto():
        nombre = gasto_nombre.get()
        try:
            importe = float(gasto_importe.get())
            if nombre and importe > 0:
                guardar_gasto(id, nombre, importe, año, mes)
            else:
                messagebox.showwarning("Advertencia", "El importe debe ser mayor que 0.")
        except ValueError:
            messagebox.showwarning("Advertencia", "El importe debe ser un número válido.")

    tk.Button(gastos_frame, text="Insertar Gasto", command=insertar_gasto, font=("Arial", 12)).pack(pady=10)
