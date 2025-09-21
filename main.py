from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel
)
import sys

# listas
autos_disponibles = []  # autos en stock
autos_vendidos = []     # autos vendidos

class Ventana(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Venta de Autos")

        layout = QVBoxLayout()

        # ---- Sección para añadir autos disponibles ----
        layout.addWidget(QLabel("Añadir Auto Disponible"))

        self.marca_disp_input = QLineEdit()
        self.marca_disp_input.setPlaceholderText("Marca del auto disponible")
        layout.addWidget(self.marca_disp_input)

        self.modelo_disp_input = QLineEdit()
        self.modelo_disp_input.setPlaceholderText("Modelo del auto disponible")
        layout.addWidget(self.modelo_disp_input)

        self.precio_disp_input = QLineEdit()
        self.precio_disp_input.setPlaceholderText("Precio del auto disponible")
        layout.addWidget(self.precio_disp_input)

        btn_agregar_disp = QPushButton("Agregar Auto Disponible")
        btn_agregar_disp.clicked.connect(self.agregar_auto_disponible)
        layout.addWidget(btn_agregar_disp)

        # ---- Sección para vender auto ----
        layout.addWidget(QLabel("Vender Auto"))

        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre del comprador")
        layout.addWidget(self.nombre_input)

        self.ci_input = QLineEdit()
        self.ci_input.setPlaceholderText("CI del comprador")
        layout.addWidget(self.ci_input)

        self.modelo_input = QLineEdit()
        self.modelo_input.setPlaceholderText("Modelo del auto a vender")
        layout.addWidget(self.modelo_input)

        btn_vender = QPushButton("Vender Auto")
        btn_vender.clicked.connect(self.vender_auto)
        layout.addWidget(btn_vender)

        # ---- Sección para listar autos ----
        botones_listar = QHBoxLayout()
        btn_listar_disp = QPushButton("Listar Autos Disponibles")
        btn_listar_disp.clicked.connect(self.listar_disponibles)
        botones_listar.addWidget(btn_listar_disp)

        btn_listar_vendidos = QPushButton("Listar Autos Vendidos")
        btn_listar_vendidos.clicked.connect(self.listar_vendidos)
        botones_listar.addWidget(btn_listar_vendidos)

        layout.addLayout(botones_listar)

        self.salida = QTextEdit()
        self.salida.setReadOnly(True)
        layout.addWidget(self.salida)

        self.setLayout(layout)

    def agregar_auto_disponible(self):
        marca = self.marca_disp_input.text().strip()
        modelo = self.modelo_disp_input.text().strip()
        precio = self.precio_disp_input.text().strip()
        if marca and modelo and precio:
            autos_disponibles.append({
                "marca": marca,
                "modelo": modelo,
                "precio": precio
            })
            self.salida.append(f"Auto disponible agregado: {marca} {modelo} - Precio: {precio}")
            self.marca_disp_input.clear()
            self.modelo_disp_input.clear()
            self.precio_disp_input.clear()
        else:
            self.salida.append("Faltan datos para agregar el auto disponible.")

    def vender_auto(self):
        nombre = self.nombre_input.text().strip()
        ci = self.ci_input.text().strip()
        modelo = self.modelo_input.text().strip()
        if nombre and ci and modelo:
            # buscar en autos disponibles por modelo
            encontrado = None
            for a in autos_disponibles:
                if a['modelo'] == modelo:
                    encontrado = a
                    break
            if encontrado:
                autos_disponibles.remove(encontrado)
                autos_vendidos.append({
                    "nombre": nombre,
                    "ci": ci,
                    "marca": encontrado['marca'],
                    "modelo": encontrado['modelo'],
                    "precio": encontrado['precio'],
                    "vendido": True
                })
                self.salida.append(
                    f"Auto {encontrado['marca']} {encontrado['modelo']} vendido a {nombre} (CI: {ci}) - Precio: {encontrado['precio']}"
                )
                self.nombre_input.clear()
                self.ci_input.clear()
                self.modelo_input.clear()
            else:
                self.salida.append(f"No hay stock del modelo {modelo}")

    def listar_disponibles(self):
        self.salida.clear()
        self.salida.append("=== AUTOS DISPONIBLES ===")
        if autos_disponibles:
            for a in autos_disponibles:
                self.salida.append(f"{a['marca']} {a['modelo']} - Precio: {a['precio']}")
        else:
            self.salida.append("No hay autos disponibles.")

    def listar_vendidos(self):
        self.salida.clear()
        self.salida.append("=== AUTOS VENDIDOS ===")
        if autos_vendidos:
            for a in autos_vendidos:
                self.salida.append(
                    f"{a['marca']} {a['modelo']} - Precio: {a['precio']} - {a['nombre']} (CI:{a['ci']}) - Vendido: {a['vendido']}"
                )
        else:
            self.salida.append("No hay autos vendidos todavía.")

# ---- Lanzar la app ----
app = QApplication(sys.argv)
ventana = Ventana()
ventana.show()
sys.exit(app.exec())
