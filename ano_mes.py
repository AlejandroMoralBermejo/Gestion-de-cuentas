import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox
from formulario import ventana_formulario
from datos import ventana_datos
import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def verificar_o_crear_registro(ano, mes):
  conexion = sqlite3.connect("datos.db")
  cursor = conexion.cursor()

  # Verificar si ya existe el registro
  cursor.execute("SELECT id FROM registros WHERE ano = ? AND mes = ?", (ano, mes))
  registro = cursor.fetchone()

  if registro:
    conexion.close()
    return registro[0]
  else:
    # Crear nuevo registro si no existe
    cursor.execute("INSERT INTO registros (ano, mes) VALUES (?, ?)", (ano, mes))
    conexion.commit()
    nuevo_id = cursor.lastrowid
    conexion.close()
    return nuevo_id


import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from tkinter import messagebox


def obtener_ingresos_gastos(ano, mes):
  conn = sqlite3.connect('datos.db')
  cursor = conn.cursor()

  cursor.execute("SELECT id, total FROM registros WHERE ano = ? AND mes = ?", (ano, mes))
  registro = cursor.fetchone()

  if not registro:
    conn.close()
    return [], [], None

  registro_id = registro[0]
  total = registro[1]

  cursor.execute("SELECT nombre, importe FROM ingresos WHERE registro_id = ?", (registro_id,))
  ingresos = cursor.fetchall()

  cursor.execute("SELECT nombre, importe FROM gastos WHERE registro_id = ?", (registro_id,))
  gastos = cursor.fetchall()

  conn.close()
  return ingresos, gastos, total


def generar_pdf(ano, mes):
  ingresos, gastos, total = obtener_ingresos_gastos(ano, mes)

  if not ingresos and not gastos:
    messagebox.showwarning("Sin datos", f"No hay datos disponibles para {mes}/{ano}.")
    return

  archivo_guardar = filedialog.asksaveasfilename(
    defaultextension=".pdf",
    filetypes=[("PDF Files", "*.pdf")],
    initialfile=f"informe_{ano}_{mes}.pdf"
  )

  # Si el usuario cancela el diálogo, no se guarda el archivo
  if not archivo_guardar:
    return

  c = canvas.Canvas(archivo_guardar, pagesize=letter)

  c.setFont("Helvetica", 12)

  c.drawString(200, 750, f"Informe de Cuentas - {mes}/{ano}")

  c.drawString(50, 700, "Ingresos:")
  y = 680
  for concepto, importe in ingresos:
    c.drawString(50, y, f"{concepto}: {importe}€")
    y -= 20

  c.drawString(50, y - 10, "Gastos:")
  y -= 30
  for concepto, importe in gastos:
    c.drawString(50, y, f"{concepto}: {importe}€")
    y -= 20

  y -= 30
  c.drawString(50, y, f"Total: {total}€")

  c.save()


def ventana_ano_mes():
  ventana = tk.Toplevel()
  ventana.title("Año y Mes")
  ventana.geometry("500x400")
  ventana.configure(bg="#F5F5F5")
  ventana.resizable(False, False)

  # Título principal
  label_titulo = tk.Label(
    ventana,
    text="Selecciona un año y un mes",
    bg="#4CAF50",
    fg="white",
    font=("Arial", 14, "bold"),
    pady=20
  )
  label_titulo.pack(fill=tk.X)

  # Contenedor para centrar el contenido
  frame_contenido = tk.Frame(ventana, bg="#F5F5F5")
  frame_contenido.pack(pady=40)

  # Campo para seleccionar año
  label_ano = tk.Label(frame_contenido, text="Año:", bg="#F5F5F5", font=("Arial", 12))
  label_ano.grid(row=0, column=0, padx=10, pady=10, sticky="e")

  anios = [str(a) for a in range(2024, 2035)]
  combo_ano = ttk.Combobox(frame_contenido, values=anios, state="readonly", font=("Arial", 11))
  combo_ano.grid(row=0, column=1, padx=10, pady=10)

  # Campo para seleccionar mes
  label_mes = tk.Label(frame_contenido, text="Mes:", bg="#F5F5F5", font=("Arial", 12))
  label_mes.grid(row=1, column=0, padx=10, pady=10, sticky="e")

  meses = {
    "Enero": 1,
    "Febrero": 2,
    "Marzo": 3,
    "Abril": 4,
    "Mayo": 5,
    "Junio": 6,
    "Julio": 7,
    "Agosto": 8,
    "Septiembre": 9,
    "Octubre": 10,
    "Noviembre": 11,
    "Diciembre": 12,
  }
  combo_mes = ttk.Combobox(frame_contenido, values=list(meses.keys()), state="readonly", font=("Arial", 11))
  combo_mes.grid(row=1, column=1, padx=10, pady=10)

  # Función para procesar la selección
  def procesar_registro(ventana_destino):
    ano = combo_ano.get()
    mes_nombre = combo_mes.get()

    if not ano or not mes_nombre:
      messagebox.showwarning("Advertencia", "Por favor, selecciona un año y un mes.")
      return

    mes = meses[mes_nombre]
    id_registro = verificar_o_crear_registro(int(ano), mes)

    if ventana_destino == "formulario":
      ventana_formulario(id_registro, ano, mes)
    else:
      ventana_datos(id_registro)

  # Función para generar el PDF
  def generar_pdf_registro():
    ano = combo_ano.get()
    mes_nombre = combo_mes.get()

    if not ano or not mes_nombre:
      messagebox.showwarning("Advertencia", "Por favor, selecciona un año y un mes.")
      return

    mes = meses[mes_nombre]
    generar_pdf(int(ano), mes)

  # Botones
  frame_botones = tk.Frame(ventana, bg="#F5F5F5")
  frame_botones.pack(pady=20)

  def on_hover(event, widget, color):
    widget['bg'] = color

  def on_leave(event, widget, color):
    widget['bg'] = color

  button_ir_formulario = tk.Button(
    frame_botones,
    text="Formulario",
    command=lambda: procesar_registro("formulario"),
    bg="#4CAF50",
    fg="white",
    font=("Arial", 12, "bold"),
    padx=20,
    pady=10,
    relief="flat",
    activebackground="#45A049"
  )
  button_ir_formulario.grid(row=0, column=0, padx=20)

  button_ir_datos = tk.Button(
    frame_botones,
    text="Datos",
    command=lambda: procesar_registro("datos"),
    bg="#4CAF50",
    fg="white",
    font=("Arial", 12, "bold"),
    padx=20,
    pady=10,
    relief="flat",
    activebackground="#45A049"
  )
  button_ir_datos.grid(row=0, column=1, padx=20)

  button_generar_pdf = tk.Button(
    frame_botones,
    text="Generar PDF",
    command=generar_pdf_registro,
    bg="#2196F3",
    fg="white",
    font=("Arial", 12, "bold"),
    padx=20,
    pady=10,
    relief="flat",
    activebackground="#1976D2"
  )
  button_generar_pdf.grid(row=1, column=0, padx=20, pady=10)

  button_ir_formulario.bind("<Enter>", lambda e: on_hover(e, button_ir_formulario, "#45A049"))
  button_ir_formulario.bind("<Leave>", lambda e: on_leave(e, button_ir_formulario, "#4CAF50"))
  button_ir_datos.bind("<Enter>", lambda e: on_hover(e, button_ir_datos, "#45A049"))
  button_ir_datos.bind("<Leave>", lambda e: on_leave(e, button_ir_datos, "#4CAF50"))
  button_generar_pdf.bind("<Enter>", lambda e: on_hover(e, button_generar_pdf, "#1976D2"))
  button_generar_pdf.bind("<Leave>", lambda e: on_leave(e, button_generar_pdf, "#2196F3"))

