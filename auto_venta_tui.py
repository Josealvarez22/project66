from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Button, ContentBlock, Label
from textual.containers import Container, Vertical, Horizontal
from textual.screen import Screen

# --- Definición de Vistas/Pantallas ---

class MenuPrincipalScreen(Screen):
    """Pantalla principal de la aplicación TUI."""

    def compose(self) -> ComposeResult:
        """Define la estructura y widgets de la pantalla."""
        yield Header()
        yield Footer()

        yield Container(
            Label("🚗 SISTEMA DE VENTA DE AUTOS 🚗", id="titulo-principal"),
            Vertical(
                Button("1. Gestión de Clientes", id="btn_clientes", variant="primary"),
                Button("2. Gestión de Vehículos", id="btn_vehiculos", variant="primary"),
                Button("3. Gestión de Ventas/Contratos", id="btn_ventas", variant="primary"),
                Button("4. Salir", id="btn_salir", variant="error"),
                id="menu-vertical"
            ),
            Static("Utiliza los botones o las teclas de acceso (no implementadas en este ejemplo)."),
            id="main-container"
        )
    
    # --- Manejadores de Eventos (Simulación) ---

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Maneja el evento de presionar un botón."""
        
        if event.button.id == "btn_clientes":
            self.notify("Abriendo Gestión de Clientes...")
            # Aquí iría el código para cambiar a la pantalla de clientes:
            # self.app.push_screen(ClientesScreen())
        
        elif event.button.id == "btn_vehiculos":
            self.notify("Abriendo Gestión de Vehículos...")

        elif event.button.id == "btn_ventas":
            self.notify("Abriendo Gestión de Ventas...")
            
        elif event.button.id == "btn_salir":
            self.app.exit()


# --- Aplicación Principal ---

class AutoVentaApp(App):
    """Clase principal de la aplicación Textual."""
    
    # Definición de la pantalla inicial
    SCREENS = {"main": MenuPrincipalScreen}
    BINDINGS = [
        ("q", "quit", "Salir de la aplicación"),
    ]
    
    # Define la hoja de estilos CSS para dar un look and feel
    CSS = """
    #titulo-principal {
        text-align: center;
        font-size: 2;
        margin-bottom: 2;
        color: #00AA00; /* Verde neón para el título */
    }
    #main-container {
        align: center middle;
    }
    #menu-vertical {
        width: 30;
        height: auto;
        padding: 1;
        border: heavy $primary;
        align: center middle;
    }
    Button {
        margin: 1 0;
        width: 100%;
    }
    """

    def on_mount(self) -> None:
        """Se llama cuando la aplicación se monta."""
        self.push_screen(MenuPrincipalScreen())

    def action_quit(self) -> None:
        """Maneja la acción de salir."""
        self.exit()

# --- Ejecución ---

if __name__ == "__main__":
    app = AutoVentaApp()
    app.run()