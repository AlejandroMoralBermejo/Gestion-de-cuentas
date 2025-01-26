import tkinter as tk
from ano_mes import ventana_ano_mes
from sqlite import inicializar_base_de_datos

if __name__ == '__main__':
    inicializar_base_de_datos()
    ventana_principal = tk.Tk()
    ventana_principal.title("Menu principal")
    ventana_principal.geometry("500x400")

    label_titulo_menu = tk.Label(
        ventana_principal,
        text="Cuentas",
        bg="#4CAF50",
        fg="white",
        padx=20,
        pady=10,
        width=200
    )
    label_titulo_menu.pack()

    boton_ingresar_consultar = tk.Button(
        ventana_principal,
        text="Ingresar/Consultar",
        command=ventana_ano_mes
    )
    boton_ingresar_consultar.place(x=70, y=200)

    ventana_principal.resizable(False,False)
    ventana_principal.mainloop()

