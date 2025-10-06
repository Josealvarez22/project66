from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QTabWidget, QTextEdit, QComboBox, QMessageBox
)
from datetime import datetime
import sys

clientes = []
vehiculos = []
ventas = []


class SistemaVentaAutos(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🚗 Sistema de Venta de Autos")
        self.setGeometry(200, 200, 700, 600)

        tabs = QTabWidget()
        tabs.addTab(self.tab_clientes(), "Clientes")
        tabs.addTab(self.tab_vehiculos(), "Vehículos")
        tabs.addTab(self.tab_ventas(), "Ventas")
        tabs.addTab(self.tab_listado(), "Listar Datos")

        layout = QVBoxLayout()
        layout.addWidget(tabs)
        self.setLayout(layout)

    # ------------------- TAB CLIENTES -------------------
    def tab_clientes(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.in_nombre = QLineEdit()
        self.in_ci = QLineEdit()
        self.in_dir = QLineEdit()
        self.in_tel = QLineEdit()
        self.in_correo = QLineEdit()

        layout.addWidget(QLabel("Nombre completo:"))
        layout.addWidget(self.in_nombre)
        layout.addWidget(QLabel("Documento de identidad:"))
        layout.addWidget(self.in_ci)
        layout.addWidget(QLabel("Dirección:"))
        layout.addWidget(self.in_dir)
        layout.addWidget(QLabel("Teléfono:"))
        layout.addWidget(self.in_tel)
        layout.addWidget(QLabel("Correo electrónico:"))
        layout.addWidget(self.in_correo)

        btn = QPushButton("Registrar Cliente")
        btn.clicked.connect(self.registrar_cliente)
        layout.addWidget(btn)

        tab.setLayout(layout)
        return tab

    def registrar_cliente(self):
        cliente = {
            "nombre": self.in_nombre.text(),
            "ci": self.in_ci.text(),
            "direccion": self.in_dir.text(),
            "telefono": self.in_tel.text(),
            "correo": self.in_correo.text(),
            "historial": []
        }
        clientes.append(cliente)
        QMessageBox.information(self, "Éxito", f"Cliente {cliente['nombre']} registrado correctamente.")
        self.in_nombre.clear()
        self.in_ci.clear()
        self.in_dir.clear()
        self.in_tel.clear()
        self.in_correo.clear()

    # ------------------- TAB VEHÍCULOS -------------------
    def tab_vehiculos(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.v_marca = QLineEdit()
        self.v_modelo = QLineEdit()
        self.v_año = QLineEdit()
        self.v_vin = QLineEdit()
        self.v_motor = QLineEdit()
        self.v_color = QLineEdit()
        self.v_precio = QLineEdit()
        self.v_estado = QComboBox()
        self.v_estado.addItems(["Nuevo", "Usado"])

        layout.addWidget(QLabel("Marca:"))
        layout.addWidget(self.v_marca)
        layout.addWidget(QLabel("Modelo:"))
        layout.addWidget(self.v_modelo)
        layout.addWidget(QLabel("Año:"))
        layout.addWidget(self.v_año)
        layout.addWidget(QLabel("N° Chasis (VIN):"))
        layout.addWidget(self.v_vin)
        layout.addWidget(QLabel("N° Motor:"))
        layout.addWidget(self.v_motor)
        layout.addWidget(QLabel("Color:"))
        layout.addWidget(self.v_color)
        layout.addWidget(QLabel("Precio:"))
        layout.addWidget(self.v_precio)
        layout.addWidget(QLabel("Estado:"))
        layout.addWidget(self.v_estado)

        btn = QPushButton("Registrar Vehículo")
        btn.clicked.connect(self.registrar_vehiculo)
        layout.addWidget(btn)

        tab.setLayout(layout)
        return tab

    def registrar_vehiculo(self):
        vehiculo = {
            "marca": self.v_marca.text(),
            "modelo": self.v_modelo.text(),
            "año": self.v_año.text(),
            "vin": self.v_vin.text(),
            "motor": self.v_motor.text(),
            "color": self.v_color.text(),
            "precio": self.v_precio.text(),
            "estado": self.v_estado.currentText(),
            "vendido": False
        }
        vehiculos.append(vehiculo)
        QMessageBox.information(self, "Éxito", f"Vehículo {vehiculo['marca']} {vehiculo['modelo']} registrado.")
        self.v_marca.clear()
        self.v_modelo.clear()
        self.v_año.clear()
        self.v_vin.clear()
        self.v_motor.clear()
        self.v_color.clear()
        self.v_precio.clear()

    # ------------------- TAB VENTAS -------------------
    def tab_ventas(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.v_ci = QLineEdit()
        self.v_modelo_auto = QLineEdit()
        self.v_contrato = QLineEdit()
        self.v_pago = QComboBox()
        self.v_pago.addItems(["Contado", "Crédito", "Leasing"])
        self.v_cuotas = QLineEdit()
        self.v_impuestos = QLineEdit()
        self.v_garantia = QLineEdit()

        layout.addWidget(QLabel("CI del comprador:"))
        layout.addWidget(self.v_ci)
        layout.addWidget(QLabel("Modelo del auto a vender:"))
        layout.addWidget(self.v_modelo_auto)
        layout.addWidget(QLabel("N° Contrato:"))
        layout.addWidget(self.v_contrato)
        layout.addWidget(QLabel("Forma de pago:"))
        layout.addWidget(self.v_pago)
        layout.addWidget(QLabel("Cuotas (si aplica):"))
        layout.addWidget(self.v_cuotas)
        layout.addWidget(QLabel("Impuestos y tasas (Bs):"))
        layout.addWidget(self.v_impuestos)
        layout.addWidget(QLabel("Garantía / Póliza:"))
        layout.addWidget(self.v_garantia)

        btn = QPushButton("Registrar Venta")
        btn.clicked.connect(self.registrar_venta)
        layout.addWidget(btn)

        tab.setLayout(layout)
        return tab

    def registrar_venta(self):
        ci = self.v_ci.text()
        cliente = next((c for c in clientes if c["ci"] == ci), None)
        if not cliente:
            QMessageBox.warning(self, "Error", "Cliente no encontrado. Regístrelo primero.")
            return

        modelo = self.v_modelo_auto.text()
        vehiculo = next((v for v in vehiculos if v["modelo"] == modelo and not v["vendido"]), None)
        if not vehiculo:
            QMessageBox.warning(self, "Error", "Vehículo no disponible o ya vendido.")
            return

        venta = {
            "contrato": self.v_contrato.text(),
            "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "cliente": cliente["nombre"],
            "vehiculo": vehiculo["modelo"],
            "forma_pago": self.v_pago.currentText(),
            "cuotas": self.v_cuotas.text(),
            "impuestos": self.v_impuestos.text(),
            "garantia": self.v_garantia.text()
        }
        ventas.append(venta)
        vehiculo["vendido"] = True
        cliente["historial"].append(venta)

        QMessageBox.information(self, "Éxito", f"Venta registrada para {cliente['nombre']} - {vehiculo['modelo']}.")
        self.v_ci.clear()
        self.v_modelo_auto.clear()
        self.v_contrato.clear()
        self.v_cuotas.clear()
        self.v_impuestos.clear()
        self.v_garantia.clear()

    # ------------------- TAB LISTADO -------------------
    def tab_listado(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        btn = QPushButton("Actualizar Listado")
        btn.clicked.connect(self.mostrar_listado)

        layout.addWidget(btn)
        layout.addWidget(self.resultado)
        tab.setLayout(layout)
        return tab

    def mostrar_listado(self):
        texto = "=== CLIENTES ===\n"
        for c in clientes:
            texto += f"{c}\n"

        texto += "\n=== VEHÍCULOS ===\n"
        for v in vehiculos:
            texto += f"{v}\n"

        texto += "\n=== VENTAS ===\n"
        for s in ventas:
            texto += f"{s}\n"

        self.resultado.setText(texto)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = SistemaVentaAutos()
    ventana.show()
    sys.exit(app.exec())
