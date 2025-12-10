
import sqlite3
import os

class DBManager:
    def __init__(self, db_name="concesionaria.db"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, db_name)

    # El resto sigue igual...
    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def crear_tablas(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        # Tabla Vehículos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vehiculos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                marca TEXT,
                modelo TEXT,
                anio INTEGER,
                vin TEXT UNIQUE,
                motor TEXT,
                color TEXT,
                precio REAL,
                estado TEXT  -- 'nuevo', 'usado', 'vendido'
            )
        ''')

        # Tabla Clientes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                documento TEXT UNIQUE,
                direccion TEXT,
                telefono TEXT,
                correo TEXT
            )
        ''')

        # Tabla Ventas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nro_contrato TEXT UNIQUE,
                fecha TEXT,
                forma_pago TEXT,
                cuotas INTEGER,
                impuestos REAL,
                garantia TEXT,
                id_cliente INTEGER,
                id_vehiculo INTEGER,
                FOREIGN KEY(id_cliente) REFERENCES clientes(id),
                FOREIGN KEY(id_vehiculo) REFERENCES vehiculos(id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("Base de datos inicializada correctamente.")