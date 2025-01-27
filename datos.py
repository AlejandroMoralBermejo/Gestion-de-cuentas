import tkinter as tk
from tkinter import ttk
import sqlite3

def cargar_datos(año, mes):
    conn = sqlite3.connect('datos.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT 
            g.nombre AS gasto_concepto,
            g.importe AS gasto_importe,
            i.nombre AS ingreso_concepto, 
            i.importe AS ingreso_importe,
            r.total AS registro_total
        FROM registros r
        LEFT JOIN (
            SELECT registro_id, nombre, importe
            FROM gastos
        ) g ON r.id = g.registro_id
        LEFT JOIN ingresos i ON r.id = i.registro_id
        WHERE r.ano = ? AND r.mes = ?
    ''', (año, mes))

    datos = cursor.fetchall()

    for dato in datos:
        print(dato)

    conn.close()
    return datos

def obtener_total(id_registro):
    connexion = sqlite3.connect("datos.db")
    cursor = connexion.cursor()

    cursor.execute(
        '''
        SELECT registros.total
        FROM registros
        WHERE registros.id = ?
        ''', (id_registro,))

    total = cursor.fetchone()

    connexion.close()
    return total

def obtener_gastos(id_registro):
    connexion = sqlite3.connect("datos.db")
    cursor = connexion.cursor()

    cursor.execute(
        '''
        SELECT gastos.nombre, gastos.importe
        FROM gastos
        WHERE gastos.registro_id = ?
        ''', (id_registro,))

    datos = cursor.fetchall()

    connexion.close()
    return datos

def obtener_ingresos(id_registro):
    connexion = sqlite3.connect("datos.db")
    cursor = connexion.cursor()

    cursor.execute(
        '''
        SELECT ingresos.nombre, ingresos.importe
        FROM ingresos
        WHERE ingresos.registro_id = ?
        ''', (id_registro,))

    datos = cursor.fetchall()

    connexion.close()
    return datos

def ventana_datos(id_registro):
    root = tk.Toplevel()
    root.title("Tabla de Gastos e Ingresos")
    root.geometry("950x700")

    # Establecer un color de fondo similar al de ventana_formulario
    root.config(bg="#F9F9F9")

    # Estilo para las tablas (similar a ventana_formulario)
    style = ttk.Style()
    style.configure("Custom.Treeview",
                    background="#E8F5E9",
                    fieldbackground="#B2DFDB",
                    font=("Arial", 10),
                    foreground="black",
                    borderwidth=1,
                    relief="solid")

    frame_tabla = tk.Frame(root, bg="#F9F9F9")
    frame_tabla.pack(fill=tk.BOTH, expand=True)

    # Tabla de Totales (izquierda)
    frame_total = tk.Frame(frame_tabla, bg="#F9F9F9")
    frame_total.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    tk.Label(frame_total, text="Total", font=("Arial", 14, "bold"), bg="#4CAF50", fg="white").pack(anchor=tk.N, pady=10)

    tabla_total = ttk.Treeview(frame_total, columns=("total"), show="headings", height=10, style="Custom.Treeview")
    tabla_total.column("total", anchor="center", width=120, stretch=tk.NO)
    tabla_total.heading("total", text="Total")
    tabla_total.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    total = obtener_total(id_registro)
    tabla_total.insert("", "end", values=(total,))

    # Tabla de Ingresos (centro)
    frame_ingresos = tk.Frame(frame_tabla, bg="#F9F9F9")
    frame_ingresos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    tk.Label(frame_ingresos, text="Ingresos", font=("Arial", 14, "bold"), bg="#4CAF50", fg="white").pack(anchor=tk.N, pady=10)

    tabla_ingresos = ttk.Treeview(frame_ingresos, columns=("concepto", "importe"), show="headings", height=10, style="Custom.Treeview")
    tabla_ingresos.column("concepto", anchor="center", width=200)
    tabla_ingresos.column("importe", anchor="center", width=100, stretch=tk.NO)
    tabla_ingresos.heading("concepto", text="Concepto")
    tabla_ingresos.heading("importe", text="Importe")
    tabla_ingresos.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    datos_ingresos = obtener_ingresos(id_registro)
    for dato in datos_ingresos:
        tabla_ingresos.insert("", "end", values=(dato[0], dato[1]))

    # Tabla de Gastos (derecha)
    frame_gastos = tk.Frame(frame_tabla, bg="#F9F9F9")
    frame_gastos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    tk.Label(frame_gastos, text="Gastos", font=("Arial", 14, "bold"), bg="#4CAF50", fg="white").pack(anchor=tk.N, pady=10)

    tabla_gastos = ttk.Treeview(frame_gastos, columns=("concepto", "importe"), show="headings", height=10, style="Custom.Treeview")
    tabla_gastos.column("concepto", anchor="center", width=200)
    tabla_gastos.column("importe", anchor="center", width=100, stretch=tk.NO)
    tabla_gastos.heading("concepto", text="Concepto")
    tabla_gastos.heading("importe", text="Importe")
    tabla_gastos.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    datos_gastos = obtener_gastos(id_registro)
    for dato in datos_gastos:
        tabla_gastos.insert("", "end", values=(dato[0], dato[1]))

    root.resizable(True, True)


