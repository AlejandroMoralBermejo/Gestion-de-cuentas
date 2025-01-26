import sqlite3

def inicializar_base_de_datos():
  conn = sqlite3.connect('datos.db')

  cursor = conn.cursor()

  cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS registros (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      ano INTEGER NOT NULL,
      mes INTEGER NOT NULL,
      total REAL DEFAULT 0
    )
    '''
  )

  cursor.execute('''
  CREATE TABLE IF NOT EXISTS gastos (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      nombre TEXT NOT NULL,
      importe REAL NOT NULL,
      registro_id INTEGER,
      FOREIGN KEY (registro_id) REFERENCES registros(id)
    )
  ''')

  cursor.execute('''
    CREATE TABLE IF NOT EXISTS ingresos (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      nombre TEXT NOT NULL,
      importe REAL NOT NULL,
      registro_id INTEGER,
      FOREIGN KEY (registro_id) REFERENCES registros(id)
    )
    '''
                 )

  conn.commit()
  conn.close()
