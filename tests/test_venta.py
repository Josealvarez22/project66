# tests/test_venta.py
import unittest
import os
import sys

# Ajuste de ruta
sys.path.append(os.getcwd())

from controllers.venta_controller import VentaController
from controllers.vehiculo_controller import VehiculoController
from controllers.cliente_controller import ClienteController
from models.venta import Venta
from models.vehiculo import Vehiculo
from models.cliente import Cliente
from database.db_manager import DBManager

class TestVenta(unittest.TestCase):
    
    def setUp(self):
        # Usamos una base de datos de prueba nueva
        self.nombre_db = "test_ventas.sqlite"
        self.db_manager = DBManager(self.nombre_db)
        self.db_manager.crear_tablas()
        
        # Inicializamos los controladores conectándolos a esa BD de prueba
        self.ctrl_venta = VentaController()
        self.ctrl_venta.db = self.db_manager
        
        self.ctrl_vehiculo = VehiculoController()
        self.ctrl_vehiculo.db = self.db_manager

        self.ctrl_cliente = ClienteController()
        self.ctrl_cliente.db = self.db_manager

    def test_registrar_venta_y_descontar_stock(self):
        """
        Prueba que al vender:
        1. La venta se guarde.
        2. El auto cambie su estado a 'vendido'.
        """
        # A. PREPARAR (Crear datos falsos necesarios)
        # 1. Necesitamos un Auto
        auto = Vehiculo("Kia", "Rio", 2024, "VIN999", "1.4", "Azul", 18000.0)
        self.ctrl_vehiculo.guardar_vehiculo(auto)
        # Obtenemos el ID del auto recién creado (sabemos que es el 1 porque la BD está vacía)
        id_auto = 1

        # 2. Necesitamos un Cliente
        cliente = Cliente("Ana", "123456", "Calle 1", "555-555", "ana@mail.com")
        self.ctrl_cliente.guardar_cliente(cliente)
        id_cliente = 1

        # B. ACTUAR (Intentar vender)
        nueva_venta = Venta(
            nro_contrato="CTR-001",
            fecha="2024-01-01",
            forma_pago="Contado",
            cuotas=0, impuestos=0, garantia="1 Año",
            id_cliente=id_cliente,
            id_vehiculo=id_auto
        )
        
        exito, msg = self.ctrl_venta.registrar_venta(nueva_venta)

        # C. VERIFICAR (Asserts)
        # 1. ¿Dijo que sí?
        self.assertTrue(exito, f"La venta falló con mensaje: {msg}")

        # 2. ¿El auto cambió de estado? (La prueba de fuego)
        # Buscamos el auto en la BD de nuevo
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT estado FROM vehiculos WHERE id=?", (id_auto,))
        estado_nuevo = cursor.fetchone()[0]
        conn.close()

        self.assertEqual(estado_nuevo, "vendido", "El auto debería marcarse como 'vendido' después de la venta")

    def tearDown(self):
        # Borrar la BD al terminar
        if os.path.exists(os.path.join("database", self.nombre_db)):
            try:
                os.remove(os.path.join("database", self.nombre_db))
            except:
                pass

if __name__ == '__main__':
    unittest.main()