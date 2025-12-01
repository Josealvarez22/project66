
from database.db_manager import DBManager
from models.venta import Venta

class VentaController:
    def __init__(self):
        self.db = DBManager()

    def registrar_venta(self, venta: Venta):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
          
            cursor.execute("SELECT estado FROM vehiculos WHERE id = ?", (venta.id_vehiculo,))
            resultado = cursor.fetchone()
            
            if not resultado:
                return False, "El vehículo no existe."
            
            if resultado[0] == 'vendido':
                return False, "ERROR: Este vehículo YA fue vendido anteriormente."

            
            cursor.execute('''
                INSERT INTO ventas (nro_contrato, fecha, forma_pago, cuotas, impuestos, garantia, id_cliente, id_vehiculo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (venta.nro_contrato, venta.fecha, venta.forma_pago, venta.cuotas, 
                  venta.impuestos, venta.garantia, venta.id_cliente, venta.id_vehiculo))

           
            cursor.execute("UPDATE vehiculos SET estado = 'vendido' WHERE id = ?", (venta.id_vehiculo,))

            conn.commit()
            return True, "¡Venta registrada con éxito!"

        except Exception as e:
            conn.rollback() 
            return False, f"Error en la venta: {e}"
        finally:
            conn.close()