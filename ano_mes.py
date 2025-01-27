import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from formulario import ventana_formulario
from datos import ventana_datos
import sqlite3


def verificar_o_crear_registro(ano, mes):
  conexion = sqlite3.connect("datos.db")
  cursor = conexion.cursor()

  # Verificar si ya existe el registro
  cursor.execute("SELECT id FROM registros WHERE ano = ? AND mes = ?", (ano, mes))
  registro = cursor.fetchone()

  if registro:
    # Si el registro ya existe, devolver el id
    conexion.close()
    return registro[0]
  else:
    # Si no existe, crear el nuevo registro y devolver el id
    cursor.execute("INSERT INTO registros (ano, mes) VALUES (?, ?)", (ano, mes))
    conexion.commit()
    nuevo_id = cursor.lastrowid  # Obtener el id del último registro insertado
    conexion.close()
    return nuevo_id


def ventana_ano_mes():
  ventana = tk.Toplevel()
  ventana.title("Año y mes")
  ventana.geometry("650x600")

  label_titulo = tk.Label(
    ventana,
    text="Selecciona un año y un mes",
    bg="#4CAF50",
    fg="white",
    padx=20,
    pady=10,
    width=200
  )
  label_titulo.pack()

  label_ano = tk.Label(ventana, text="Año: ")
  label_ano.place(x=70, y=200)

  anios = [str(a) for a in range(2024, 2035)]

  combo_ano = ttk.Combobox(ventana, values=anios, state="readonly")
  combo_ano.place(x=120, y=200)

  label_mes = tk.Label(ventana, text="Mes:")
  label_mes.place(x=370, y=200)

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

  combo_mes = ttk.Combobox(ventana, values=list(meses.keys()), state="readonly")
  combo_mes.place(x=420, y=200)

  def procesar_registro(ventana):
    ano = combo_ano.get()
    mes_nombre = combo_mes.get()

    if not ano or not mes_nombre:
      messagebox.showwarning("Advertencia", "Por favor, selecciona un año y un mes.")
      return

    mes = meses[mes_nombre]  # Obtener el número del mes
    id = verificar_o_crear_registro(int(ano), mes)

    if ventana == "formulario":
      ventana_formulario(id, ano, mes)
    else:
      ventana_datos(id)


  button_ir_formulario = tk.Button(ventana, text="Formulario", command=lambda: procesar_registro("formulario"))
  button_ir_formulario.place(x=150, y=400)

  button_ir_datos = tk.Button(ventana, text="Datos", command=lambda: procesar_registro("datos"))
  button_ir_datos.place(x=450, y=400)

  ventana.resizable(False,False)