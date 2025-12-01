
from database.db_manager import DBManager
from models.cliente import Cliente

class ClienteController:
    def __init__(self):
        self.db = DBManager()

    def guardar_cliente(self, cliente: Cliente):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO clientes (nombre, documento, direccion, telefono, correo) VALUES (?, ?, ?, ?, ?)",
                           (cliente.nombre, cliente.documento, cliente.direccion, cliente.telefono, cliente.correo))
            conn.commit()
            return True, "Cliente guardado."
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes")
        datos = cursor.fetchall()
        conn.close()
        return datos