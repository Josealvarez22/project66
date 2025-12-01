import json
import os
from datetime import datetime

from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Header, Footer, Button, DataTable, Input, Label, Static
from textual.screen import Screen
from textual.message import Message
from textual.binding import Binding
from rich.text import Text  # Usamos Rich para colorear texto de forma segura

# ==========================================
# 1. GESTIÓN DE DATOS (Incluida en el mismo archivo)
# ==========================================

DATA_FILE = "auto_venta_data.json"

# Estructura inicial en memoria
db = {
    'clientes': [],
    'vehiculos': []
}

def cargar_datos():
    """Carga datos del JSON."""
    global db
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    db.update(json.loads(content))
                    return True
        except Exception:
            return False
    return False

def guardar_datos():
    """Guarda datos en el JSON."""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(db, f, indent=4)
        return True
    except Exception:
        return False

def get_next_id(lista):
    return max([item['id'] for item in lista] or [0]) + 1

def add_cliente(nombre, telefono, email):
    nuevo = {
        'id': get_next_id(db['clientes']),
        'nombre': nombre,
        'telefono': telefono,
        'email': email
    }
    db['clientes'].append(nuevo)
    guardar_datos()
    return nuevo

def add_vehiculo(marca, modelo, anio, precio):
    nuevo = {
        'id': get_next_id(db['vehiculos']),
        'marca': marca,
        'modelo': modelo,
        'anio': anio,
        'precio': precio,
        'estado': 'Disponible'
    }
    db['vehiculos'].append(nuevo)
    guardar_datos()
    return nuevo

def update_vehiculo_status(vehiculo_id, nuevo_estado):
    for v in db['vehiculos']:
        if v['id'] == vehiculo_id:
            v['estado'] = nuevo_estado
            guardar_datos()
            return v
    return None

def update_vehiculo_data(vehiculo_id, marca, modelo, anio, precio):
    for v in db['vehiculos']:
        if v['id'] == vehiculo_id:
            v['marca'] = marca
            v['modelo'] = modelo
            v['anio'] = anio
            v['precio'] = precio
            guardar_datos()
            return v
    return None

# ==========================================
# 2. INTERFAZ DE USUARIO (TUI)
# ==========================================

class ClientesForm(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Cancelar")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Label("Nombre Completo:"),
            Input(placeholder="Ej: Juan Pérez", id="nombre"),
            Label("Teléfono:"),
            Input(placeholder="Ej: 70012345", id="telefono"),
            Label("Email:"),
            Input(placeholder="Ej: juan@mail.com", id="email"),
            Button("Guardar Cliente", variant="success", id="btn_save"),
            classes="form_box"
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "btn_save":
            nom = self.query_one("#nombre", Input).value
            tel = self.query_one("#telefono", Input).value
            mail = self.query_one("#email", Input).value
            
            if nom and tel:
                add_cliente(nom, tel, mail)
                self.app.pop_screen()
                self.app.notify(f"Cliente {nom} guardado.")
            else:
                self.app.notify("Nombre y Teléfono requeridos.", severity="error")

class ClientesList(Screen):
    BINDINGS = [
        ("escape", "app.pop_screen", "Volver"),
        ("r", "refresh_table", "Recargar"),
        ("a", "add_client", "Añadir")
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Label("LISTA DE CLIENTES", classes="title"),
            DataTable(id="table_clientes"),
            classes="list_box"
        )
        yield Footer()

    def on_mount(self):
        self.cargar_tabla()

    def action_add_client(self):
        self.app.push_screen(ClientesForm(), lambda _: self.cargar_tabla())

    def action_refresh_table(self):
        self.cargar_tabla()

    def cargar_tabla(self):
        table = self.query_one("#table_clientes", DataTable)
        table.clear(columns=True)
        table.add_columns("ID", "Nombre", "Teléfono", "Email")
        for c in db['clientes']:
            table.add_row(c['id'], c['nombre'], c['telefono'], c['email'])

class VehiculoForm(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Cancelar")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Label("Marca:"),
            Input(placeholder="Ej: Toyota", id="marca"),
            Label("Modelo:"),
            Input(placeholder="Ej: Corolla", id="modelo"),
            Label("Año:"),
            Input(placeholder="2020", id="anio", type="integer"),
            Label("Precio:"),
            Input(placeholder="15000", id="precio", type="number"),
            Button("Guardar Vehículo", variant="success", id="btn_save_veh"),
            classes="form_box"
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "btn_save_veh":
            marca = self.query_one("#marca", Input).value
            modelo = self.query_one("#modelo", Input).value
            anio = self.query_one("#anio", Input).value
            precio = self.query_one("#precio", Input).value

            if marca and modelo:
                try:
                    add_vehiculo(marca, modelo, int(anio), float(precio))
                    self.app.pop_screen()
                    self.app.notify("Vehículo guardado.")
                except ValueError:
                    self.app.notify("Año y Precio deben ser números.", severity="error")
            else:
                self.app.notify("Marca y Modelo requeridos.", severity="error")

class VehiculoEdit(Screen):
    def __init__(self, vid):
        super().__init__()
        self.vid = vid
        self.v_data = next((v for v in db['vehiculos'] if v['id'] == vid), None)

    def compose(self) -> ComposeResult:
        if not self.v_data:
            yield Label("Error: Vehículo no encontrado")
            return

        yield Header()
        yield Container(
            Label(f"Editando ID: {self.vid}"),
            Label("Marca:"),
            Input(value=self.v_data['marca'], id="e_marca"),
            Label("Modelo:"),
            Input(value=self.v_data['modelo'], id="e_modelo"),
            Label("Año:"),
            Input(value=str(self.v_data['anio']), id="e_anio"),
            Label("Precio:"),
            Input(value=str(self.v_data['precio']), id="e_precio"),
            Button("Actualizar", variant="warning", id="btn_update"),
            classes="form_box"
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "btn_update":
            try:
                marca = self.query_one("#e_marca", Input).value
                modelo = self.query_one("#e_modelo", Input).value
                anio = int(self.query_one("#e_anio", Input).value)
                precio = float(self.query_one("#e_precio", Input).value)
                update_vehiculo_data(self.vid, marca, modelo, anio, precio)
                self.app.pop_screen()
                self.app.notify("Vehículo actualizado.")
            except ValueError:
                self.app.notify("Datos numéricos inválidos.", severity="error")

class VehiculosList(Screen):
    BINDINGS = [
        ("escape", "app.pop_screen", "Volver"),
        ("a", "add_veh", "Añadir"),
        ("s", "toggle_status", "Estado (Vender/Disp)"),
        ("e", "edit_veh", "Editar")
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Label("LISTA DE VEHÍCULOS", classes="title"),
            Label("Teclas: [A] Añadir | [S] Cambiar Estado | [E] Editar | [Clic] Seleccionar", classes="subtitle"),
            DataTable(id="table_vehiculos", cursor_type="row"),
            classes="list_box"
        )
        yield Footer()

    def on_mount(self):
        self.cargar_tabla()

    def action_add_veh(self):
        self.app.push_screen(VehiculoForm(), lambda _: self.cargar_tabla())

    def get_selected_id(self):
        table = self.query_one("#table_vehiculos", DataTable)
        try:
            # Obtiene ID de la primera celda de la fila seleccionada
            row_index = table.cursor_row
            return int(table.get_cell_at((row_index, 0)))
        except Exception:
            return None

    def action_toggle_status(self):
        vid = self.get_selected_id()
        if vid:
            v = next((x for x in db['vehiculos'] if x['id'] == vid), None)
            if v:
                nuevo = "Vendido" if v['estado'] == "Disponible" else "Disponible"
                update_vehiculo_status(vid, nuevo)
                self.cargar_tabla()
                self.app.notify(f"Estado cambiado a {nuevo}")
        else:
            self.app.notify("Selecciona un vehículo primero.", severity="warning")

    def action_edit_veh(self):
        vid = self.get_selected_id()
        if vid:
            self.app.push_screen(VehiculoEdit(vid), lambda _: self.cargar_tabla())
        else:
            self.app.notify("Selecciona un vehículo primero.", severity="warning")

    def cargar_tabla(self):
        table = self.query_one("#table_vehiculos", DataTable)
        table.clear(columns=True)
        table.add_columns("ID", "Marca", "Modelo", "Año", "Precio", "Estado")
        
        for v in db['vehiculos']:
            # Usamos Rich Text para el color, es más seguro que CSS en filas
            estado_str = v['estado']
            color = "green" if estado_str == "Disponible" else "red"
            estado_styled = Text(estado_str, style=f"bold {color}")
            
            table.add_row(
                v['id'], v['marca'], v['modelo'], v['anio'], 
                f"${v['precio']}", estado_styled
            )

class MenuPrincipal(Screen):
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Container(
            Label("🚗 GESTIÓN DE VENTA DE AUTOS 🚗", classes="main_title"),
            Button("Gestión de Clientes", id="btn_cli", variant="primary"),
            Button("Gestión de Vehículos", id="btn_veh", variant="primary"),
            Button("Salir", id="btn_exit", variant="error"),
            classes="menu_box"
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "btn_cli":
            self.app.push_screen(ClientesList())
        elif event.button.id == "btn_veh":
            self.app.push_screen(VehiculosList())
        elif event.button.id == "btn_exit":
            self.app.exit()

class SistemaAutosApp(App):
    CSS = """
    Screen { align: center middle; }
    .main_title { text-align: center; text-style: bold; color: yellow; margin-bottom: 2; }
    .title { text-align: center; color: green; text-style: bold; }
    .subtitle { text-align: center; color: gray; margin-bottom: 1; }
    .menu_box { width: 40; height: auto; border: heavy white; padding: 2; }
    .form_box { width: 50; height: auto; border: solid green; padding: 2; }
    .list_box { width: 90%; height: 80%; border: solid blue; }
    Button { width: 100%; margin-bottom: 1; }
    DataTable { height: 1fr; }
    Input { margin-bottom: 1; }
    """

    def on_mount(self):
        cargar_datos()
        self.push_screen(MenuPrincipal())

# --- BLOQUE DE EJECUCIÓN ---
if __name__ == "__main__":
    app = SistemaAutosApp()
    app.run()