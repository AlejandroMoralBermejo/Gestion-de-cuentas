import tkinter as tk
from tkinter import messagebox
import sqlite3

def actualizar_total(id_registro):
    # Conectar a la base de datos
    conn = sqlite3.connect('datos.db')
    cursor = conn.cursor()

    # Calcular ingresos totales
    cursor.execute('''
        SELECT COALESCE(SUM(i.importe), 0)
        FROM ingresos i
        WHERE i.registro_id = ?
    ''', (id_registro,))
    ingresos_totales = cursor.fetchone()[0]

    # Calcular gastos totales
    cursor.execute('''
        SELECT COALESCE(SUM(g.importe), 0)
        FROM gastos g
        WHERE g.registro_id = ?
    ''', (id_registro,))
    gastos_totales = cursor.fetchone()[0]

    # Calcular el total como ingresos - gastos
    total = ingresos_totales - gastos_totales

    print(f"Ingresos totales: {ingresos_totales}  Gastos totales: {gastos_totales}  Total: {total}")

    # Actualizar el campo total en la tabla registros
    cursor.execute('''
        UPDATE registros
        SET total = ?
        WHERE id = ?
    ''', (total, id_registro))

    conn.commit()
    conn.close()

def guardar_gasto(id_registro, nombre, importe):
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
    actualizar_total(id_registro)

    messagebox.showinfo("Éxito", "Gasto guardado exitosamente.")

def guardar_ingreso(id_registro, nombre, importe):
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
    actualizar_total(id_registro)

    messagebox.showinfo("Éxito", "Ingreso guardado exitosamente.")

def ventana_formulario(id, año, mes):
    ventana = tk.Toplevel()
    ventana.title(f"Formulario - {mes}/{año}")
    ventana.geometry("600x700")
    ventana.configure(bg="#F9F9F9")

    tk.Label(ventana, text=f"Formulario para Ingresos y Gastos ({mes}/{año})",
             font=("Arial", 16, "bold"), bg="#4CAF50", fg="white", pady=10).pack(fill=tk.X)


    ingresos_frame = tk.LabelFrame(ventana, text="Ingresos", font=("Arial", 12), padx=20, pady=20, bg="#E8F5E9")
    ingresos_frame.pack(fill="both", expand=True, padx=10, pady=5)

    tk.Label(ingresos_frame, text="Concepto", font=("Arial", 10), bg="#E8F5E9").pack(pady=5)
    ingreso_nombre = tk.Entry(ingresos_frame, font=("Arial", 10))
    ingreso_nombre.pack(pady=5)

    tk.Label(ingresos_frame, text="Importe (€)", font=("Arial", 10), bg="#E8F5E9").pack(pady=5)
    ingreso_importe = tk.Entry(ingresos_frame, font=("Arial", 10))
    ingreso_importe.pack(pady=5)

    tk.Button(ingresos_frame, text="Guardar Ingreso",
              command=lambda: [guardar_ingreso(id, ingreso_nombre.get(), float(ingreso_importe.get()))],
              font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=10)

    gastos_frame = tk.LabelFrame(ventana, text="Gastos", font=("Arial", 12), padx=20, pady=20, bg="#FFEBEE")
    gastos_frame.pack(fill="both", expand=True, padx=10, pady=5)

    tk.Label(gastos_frame, text="Concepto", font=("Arial", 10), bg="#FFEBEE").pack(pady=5)
    gasto_nombre = tk.Entry(gastos_frame, font=("Arial", 10))
    gasto_nombre.pack(pady=5)

    tk.Label(gastos_frame, text="Importe (€)", font=("Arial", 10), bg="#FFEBEE").pack(pady=5)
    gasto_importe = tk.Entry(gastos_frame, font=("Arial", 10))
    gasto_importe.pack(pady=5)

    tk.Button(gastos_frame, text="Guardar Gasto",
              command=lambda: [guardar_gasto(id, gasto_nombre.get(), float(gasto_importe.get()))],
              font=("Arial", 12), bg="#D32F2F", fg="white").pack(pady=10)


