import tkinter as tk
from tkinter import ttk
import sqlite3

def cargar_datos(año, mes):
    # Conectar a la base de datos
    conn = sqlite3.connect('datos.db')
    cursor = conn.cursor()

    # Obtener todos los gastos, ingresos y total de un solo query
    cursor.execute('''
        SELECT 
            g.nombre AS gasto_concepto, g.importe AS gasto_importe,
            i.nombre AS ingreso_concepto, i.importe AS ingreso_importe,
            r.total AS registro_total
        FROM registros r
        LEFT JOIN (
            SELECT registro_id, nombre, importe
            FROM gastos
        ) g ON r.id = g.registro_id
        LEFT JOIN ingresos i ON r.id = i.registro_id
        WHERE r.ano = ? AND r.mes = ?
    ''', (año, mes))

    # Traer todos los resultados
    datos = cursor.fetchall()
    conn.close()
    return datos

def ventana_datos(año, mes):
    root = tk.Toplevel()
    root.title("Tabla de Gastos e Ingresos")
    root.geometry("700x300")

    header_frame = tk.Frame(root)
    header_frame.pack(fill=tk.X, pady=5)

    tk.Label(header_frame, text="Gastos", font=("Arial", 12, "bold"), width=25).pack(side=tk.LEFT, padx=10)
    tk.Label(header_frame, text="Ingresos", font=("Arial", 12, "bold"), width=25).pack(side=tk.LEFT, padx=10)
    tk.Label(header_frame, text="Total", font=("Arial", 12, "bold"), width=10).pack(side=tk.RIGHT, padx=10)

    content_frame = tk.Frame(root)
    content_frame.pack(fill=tk.BOTH, expand=True)

    table = ttk.Treeview(content_frame, columns=("g_concepto", "g_importe", "i_concepto", "i_importe", "total"),
                         show="headings", height=10)

    table.column("g_concepto", anchor="center", width=150)
    table.column("g_importe", anchor="center", width=100)
    table.column("i_concepto", anchor="center", width=150)
    table.column("i_importe", anchor="center", width=100)
    table.column("total", anchor="center", width=100)

    table.heading("g_concepto", text="Concepto")
    table.heading("g_importe", text="Importe")
    table.heading("i_concepto", text="Concepto")
    table.heading("i_importe", text="Importe")
    table.heading("total", text="Total")

    # Obtener los datos de gastos, ingresos y total
    datos = cargar_datos(año, mes)

    # Insertar los datos en la tabla
    for dato in datos:
        table.insert("", "end", values=(dato[0], dato[1], dato[2], dato[3], dato[4]))

    table.pack(fill=tk.BOTH, expand=True)

    root.resizable(False, False)

