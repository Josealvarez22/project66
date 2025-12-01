
from database.db_manager import DBManager
from models.vehiculo import Vehiculo

class VehiculoController:
    def __init__(self):
        self.db = DBManager()

    def guardar_vehiculo(self, vehiculo: Vehiculo):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO vehiculos (marca, modelo, anio, vin, motor, color, precio, estado)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (vehiculo.marca, vehiculo.modelo, vehiculo.anio, vehiculo.vin, 
                  vehiculo.motor, vehiculo.color, vehiculo.precio, vehiculo.estado))
            conn.commit()
            return True, "Vehículo guardado con éxito"
        except Exception as e:
            return False, f"Error al guardar: {e}"
        finally:
            conn.close()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vehiculos")
        datos = cursor.fetchall()
        conn.close()
        return datos