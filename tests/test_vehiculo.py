import unittest
import os
import sys

# Esto ayuda a Python a encontrar tus carpetas models y controllers
sys.path.append(os.getcwd())

from controllers.vehiculo_controller import VehiculoController
from models.vehiculo import Vehiculo
from database.db_manager import DBManager

# REGLA 1: La clase debe heredar de unittest.TestCase
class TestVehiculo(unittest.TestCase):
    
    def setUp(self):
        self.nombre_db_prueba = "test_db.sqlite"
        self.controller = VehiculoController()
        self.controller.db = DBManager(self.nombre_db_prueba)
        self.controller.db.crear_tablas()

    # REGLA 2: La función DEBE empezar con "test_"
    def test_guardar_vehiculo_exitoso(self):
        # 1. Preparar
        nuevo_auto = Vehiculo("Toyota", "Corolla", 2024, "TEST12345", "1.8", "Rojo", 25000.0)

        # 2. Actuar
        exito, mensaje = self.controller.guardar_vehiculo(nuevo_auto)

        # 3. Verificar
        self.assertTrue(exito, "Debería retornar True")
        
        # Verificar que se guardó en la BD
        todos = self.controller.obtener_todos()
        self.assertEqual(len(todos), 1)
        self.assertEqual(todos[0][1], "Toyota")

    def tearDown(self):
        if os.path.exists(os.path.join("database", self.nombre_db_prueba)):
            try:
                os.remove(os.path.join("database", self.nombre_db_prueba))
            except:
                pass

if __name__ == '__main__':
    unittest.main()