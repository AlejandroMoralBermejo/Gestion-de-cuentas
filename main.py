import tkinter as tk
from ano_mes import ventana_ano_mes
from sqlite import inicializar_base_de_datos

def on_hover(event, widget, bg_color):
    widget['bg'] = bg_color

def on_leave(event, widget, bg_color):
    widget['bg'] = bg_color

if __name__ == '__main__':

    inicializar_base_de_datos()
    ventana_principal = tk.Tk()
    ventana_principal.title("Menú Principal")
    ventana_principal.geometry("500x400")
    ventana_principal.configure(bg="#F5F5F5")
    ventana_principal.resizable(False, False)

    label_titulo_menu = tk.Label(
        ventana_principal,
        text="Cuentas",
        bg="#4CAF50",
        fg="white",
        font=("Arial", 16, "bold"),
        pady=20
    )
    label_titulo_menu.pack(fill=tk.X)

    frame_botones = tk.Frame(ventana_principal, bg="#F5F5F5", pady=30)
    frame_botones.pack(expand=True)

    boton_ingresar_consultar = tk.Button(
        frame_botones,
        text="Ingresar/Consultar",
        command=ventana_ano_mes,
        bg="#4CAF50",
        fg="white",
        font=("Arial", 12, "bold"),
        padx=20,
        pady=10,
        relief="flat",
        activebackground="#45A049"
    )
    boton_ingresar_consultar.grid(row=0, column=0, pady=10)

    boton_ingresar_consultar.bind("<Enter>", lambda e: on_hover(e, boton_ingresar_consultar, "#45A049"))
    boton_ingresar_consultar.bind("<Leave>", lambda e: on_leave(e, boton_ingresar_consultar, "#4CAF50"))

    ventana_principal.mainloop()
