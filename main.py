from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QTextEdit, QLineEdit
)
import sys

class TerminalAutos(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Terminal - Sistema de Venta de Autos")

        # Layout vertical
        self.layout = QVBoxLayout()

        # Área de salida (texto)
        self.output = QTextEdit()
        self.output.setReadOnly(True)

        # Línea de entrada para escribir comandos
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Escribe un comando y presiona Enter…")
        self.input_line.returnPressed.connect(self.ejecutar_comando)

        # Añadir widgets al layout
        self.layout.addWidget(self.output)
        self.layout.addWidget(self.input_line)
        self.setLayout(self.layout)

        # Lista de autos registrados
        self.autos = []

        self.output.append("Comandos disponibles:")
        self.output.append("  agregar <marca> <modelo> <precio>")
        self.output.append("  listar")
        self.output.append("  salir")

    def ejecutar_comando(self):
        comando = self.input_line.text().strip()
        self.input_line.clear()
        self.output.append(f"> {comando}")
        partes = comando.split()

        if not partes:
            return

        if partes[0] == "agregar":
            # Ejemplo: agregar Toyota Corolla 15000
            if len(partes) >= 4:
                marca = partes[1]
                modelo = partes[2]
                precio = partes[3]
                self.autos.append((marca, modelo, precio))
                self.output.append(f"Auto agregado: {marca} {modelo} - ${precio}")
            else:
                self.output.append("Uso: agregar <marca> <modelo> <precio>")

        elif partes[0] == "listar":
            if self.autos:
                self.output.append("Autos registrados:")
                for i, auto in enumerate(self.autos, 1):
                    self.output.append(f"{i}. {auto[0]} {auto[1]} - ${auto[2]}")
            else:
                self.output.append("No hay autos registrados.")

        elif partes[0] == "salir":
            self.output.append("Saliendo…")
            QApplication.quit()

        else:
            self.output.append("Comando no reconocido. Usa: agregar, listar, salir.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = TerminalAutos()
    ventana.resize(600, 400)
    ventana.show()
    sys.exit(app.exec())
