
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


from controllers.vehiculo_controller import VehiculoController
from controllers.cliente_controller import ClienteController
from controllers.venta_controller import VentaController 

from models.vehiculo import Vehiculo
from models.cliente import Cliente
from models.venta import Venta 

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión Automotriz")
        self.geometry("1000x650")

        # Inicia controladores
        self.vehiculo_controller = VehiculoController()
        self.cliente_controller = ClienteController()
        self.venta_controller = VentaController() #INICIA

  
        self.lista_clientes_ids = []
        self.lista_vehiculos_ids = []

 
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)

        self.tab_vehiculos = tk.Frame(self.notebook)
        self.tab_clientes = tk.Frame(self.notebook)
        self.tab_ventas = tk.Frame(self.notebook)

        self.notebook.add(self.tab_vehiculos, text=" 🚗 Inventario Vehículos ")
        self.notebook.add(self.tab_clientes, text=" 👥 Clientes ")
        self.notebook.add(self.tab_ventas, text=" 💰 Nueva Venta ")

        # Evento: Cuando cambies de pestaña, actualiza los datos
        self.notebook.bind("<<NotebookTabChanged>>", self.al_cambiar_pestana)

        self.setup_pestana_vehiculos()
        self.setup_pestana_clientes()
        self.setup_pestana_ventas()

    def al_cambiar_pestana(self, event):

        id_pestana = self.notebook.index("current")
        if id_pestana == 2: 
            self.cargar_combos_ventas()

    
    def setup_pestana_vehiculos(self):
        # Formulario
        frame_form = tk.LabelFrame(self.tab_vehiculos, text="Registrar Auto", padx=10, pady=10)
        frame_form.pack(side="left", fill="y", padx=10, pady=10)

        tk.Label(frame_form, text="Marca:").pack(anchor="w")
        self.entry_v_marca = tk.Entry(frame_form)
        self.entry_v_marca.pack(fill="x")

        tk.Label(frame_form, text="Modelo:").pack(anchor="w")
        self.entry_v_modelo = tk.Entry(frame_form)
        self.entry_v_modelo.pack(fill="x")

        tk.Label(frame_form, text="VIN:").pack(anchor="w")
        self.entry_v_vin = tk.Entry(frame_form)
        self.entry_v_vin.pack(fill="x")

        tk.Label(frame_form, text="Precio:").pack(anchor="w")
        self.entry_v_precio = tk.Entry(frame_form)
        self.entry_v_precio.pack(fill="x")

        tk.Button(frame_form, text="Guardar", command=self.guardar_vehiculo, bg="#4CAF50", fg="white").pack(pady=15, fill="x")

        # Tabla
        frame_tabla = tk.Frame(self.tab_vehiculos)
        frame_tabla.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.tree_vehiculos = ttk.Treeview(frame_tabla, columns=("ID", "Marca", "Modelo", "VIN", "Precio", "Estado"), show="headings")
        for col in ("ID", "Marca", "Modelo", "VIN", "Precio", "Estado"):
            self.tree_vehiculos.heading(col, text=col)
            self.tree_vehiculos.column(col, width=100)
        
        self.tree_vehiculos.pack(fill="both", expand=True)
        tk.Button(frame_tabla, text="Actualizar Lista", command=self.cargar_lista_vehiculos).pack(fill="x")
        self.cargar_lista_vehiculos()

    def guardar_vehiculo(self):
        try:
            v = Vehiculo(self.entry_v_marca.get(), self.entry_v_modelo.get(), 2024, 
                         self.entry_v_vin.get(), "N/A", "N/A", float(self.entry_v_precio.get()))
            ok, msg = self.vehiculo_controller.guardar_vehiculo(v)
            if ok:
                messagebox.showinfo("Éxito", msg)
                self.cargar_lista_vehiculos()
                # Limpia
                self.entry_v_marca.delete(0, 'end')
                self.entry_v_modelo.delete(0, 'end')
                self.entry_v_vin.delete(0, 'end')
                self.entry_v_precio.delete(0, 'end')
            else:
                messagebox.showerror("Error", msg)
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser numérico")

    def cargar_lista_vehiculos(self):
        for item in self.tree_vehiculos.get_children():
            self.tree_vehiculos.delete(item)
        datos = self.vehiculo_controller.obtener_todos()
        for d in datos:
          
            estado = d[8]
            vals = (d[0], d[1], d[2], d[4], d[7], estado)
            
            # Insertar en tabla
            item_id = self.tree_vehiculos.insert("", "end", values=vals)
            
           
            if estado == 'vendido':
                self.tree_vehiculos.item(item_id, tags=('vendido',))
        
        self.tree_vehiculos.tag_configure('vendido', background='#ffcccc') # Fondo rojo claro

   
    def setup_pestana_clientes(self):
        frame_form = tk.LabelFrame(self.tab_clientes, text="Registrar Cliente", padx=10, pady=10)
        frame_form.pack(side="left", fill="y", padx=10, pady=10)

        tk.Label(frame_form, text="Nombre:").pack(anchor="w")
        self.entry_c_nombre = tk.Entry(frame_form)
        self.entry_c_nombre.pack(fill="x")

        tk.Label(frame_form, text="Documento:").pack(anchor="w")
        self.entry_c_doc = tk.Entry(frame_form)
        self.entry_c_doc.pack(fill="x")
        
        tk.Label(frame_form, text="Teléfono:").pack(anchor="w")
        self.entry_c_tel = tk.Entry(frame_form)
        self.entry_c_tel.pack(fill="x")

        tk.Button(frame_form, text="Guardar", command=self.guardar_cliente, bg="#2196F3", fg="white").pack(pady=15, fill="x")

        # Tabla Clientes
        frame_tabla = tk.Frame(self.tab_clientes)
        frame_tabla.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        self.tree_clientes = ttk.Treeview(frame_tabla, columns=("ID", "Nombre", "Documento", "Tel"), show="headings")
        for col in ("ID", "Nombre", "Documento", "Tel"):
            self.tree_clientes.heading(col, text=col)
        self.tree_clientes.pack(fill="both", expand=True)
        self.cargar_lista_clientes()

    def guardar_cliente(self):
        c = Cliente(self.entry_c_nombre.get(), self.entry_c_doc.get(), "N/A", self.entry_c_tel.get(), "N/A")
        ok, msg = self.cliente_controller.guardar_cliente(c)
        if ok:
            messagebox.showinfo("Éxito", msg)
            self.cargar_lista_clientes()
            self.entry_c_nombre.delete(0, 'end')
            self.entry_c_doc.delete(0, 'end')
            self.entry_c_tel.delete(0, 'end')
        else:
            messagebox.showerror("Error", msg)

    def cargar_lista_clientes(self):
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
        datos = self.cliente_controller.obtener_todos()
        for d in datos:
            self.tree_clientes.insert("", "end", values=(d[0], d[1], d[2], d[4]))


    def setup_pestana_ventas(self):
        # Cont principal 
        main_frame = tk.Frame(self.tab_ventas, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        tk.Label(main_frame, text="REGISTRAR NUEVA VENTA", font=("Arial", 14, "bold")).pack(pady=10)

        #  formulario
        form_frame = tk.Frame(main_frame)
        form_frame.pack()

        # Selección Cliente
        tk.Label(form_frame, text="Seleccionar Cliente:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.combo_clientes = ttk.Combobox(form_frame, width=40, state="readonly")
        self.combo_clientes.grid(row=0, column=1, padx=5, pady=5)

        # Selección de los Vehículos
        tk.Label(form_frame, text="Seleccionar Vehículo:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.combo_vehiculos = ttk.Combobox(form_frame, width=40, state="readonly")
        self.combo_vehiculos.grid(row=1, column=1, padx=5, pady=5)

        # Datos de las Ventass
        tk.Label(form_frame, text="Nro Contrato:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_contrato = tk.Entry(form_frame, width=43)
        self.entry_contrato.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Forma de Pago:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.combo_pago = ttk.Combobox(form_frame, values=["Contado", "Crédito", "Leasing"], state="readonly", width=40)
        self.combo_pago.current(0)
        self.combo_pago.grid(row=3, column=1, padx=5, pady=5)

        # Botón Acción
        btn_vender = tk.Button(main_frame, text="Confirmar Venta", bg="#FF5722", fg="white", font=("Arial", 11), height=2, width=20, command=self.accion_vender)
        btn_vender.pack(pady=30)

        tk.Label(main_frame, text="Nota: Al confirmar, el stock del auto se descontará automáticamente.", fg="gray").pack()

    def cargar_combos_ventas(self):
        """Carga los clientes y autos disponibles en los Combobox"""
        
        # 1. Cargar Clientes
        clientes = self.cliente_controller.obtener_todos()
        self.lista_clientes_ids = [] # Guardamos los IDs
        display_clientes = []
        
        for c in clientes:
            
            self.lista_clientes_ids.append(c[0])
            display_clientes.append(f"{c[1]} - Doc: {c[2]}")
        
        self.combo_clientes['values'] = display_clientes
        if display_clientes: self.combo_clientes.current(0)

        # 2. Cargar Vehículos 
        vehiculos = self.vehiculo_controller.obtener_todos()
        self.lista_vehiculos_ids = []
        display_vehiculos = []

        for v in vehiculos:
            
            if v[8] != 'vendido': # muestra los NO vendidos
                self.lista_vehiculos_ids.append(v[0])
                display_vehiculos.append(f"{v[1]} {v[2]} - ${v[7]} ({v[8]})")
        
        self.combo_vehiculos['values'] = display_vehiculos
        if display_vehiculos: 
            self.combo_vehiculos.current(0)
        else:
            self.combo_vehiculos.set("No hay autos disponibles")

    def accion_vender(self):
        # Validacion
        idx_cliente = self.combo_clientes.current()
        idx_vehiculo = self.combo_vehiculos.current()

        if idx_cliente == -1 or idx_vehiculo == -1:
            messagebox.showwarning("Atención", "Seleccione un cliente y un vehículo")
            return

        if not self.lista_vehiculos_ids:
            messagebox.showwarning("Error", "No hay vehículos disponibles para vender")
            return

        # Obtener ID
        id_cliente_real = self.lista_clientes_ids[idx_cliente]
        id_vehiculo_real = self.lista_vehiculos_ids[idx_vehiculo]

        # Crear Venta
        nueva_venta = Venta(
            nro_contrato=self.entry_contrato.get(),
            fecha=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            forma_pago=self.combo_pago.get(),
            cuotas=0, impuestos=0.0, garantia="1 Año",
            id_cliente=id_cliente_real,
            id_vehiculo=id_vehiculo_real
        )

    
        exito, mensaje = self.venta_controller.registrar_venta(nueva_venta)

        if exito:
            messagebox.showinfo("Felicidades", mensaje)
            self.entry_contrato.delete(0, 'end')
            # Recargar lista de vehículos si estan o no disponible
            self.cargar_combos_ventas()
            self.cargar_lista_vehiculos()
        else:
            messagebox.showerror("Error", mensaje)