class Cliente:
    def __init__(self, nombre, documento, direccion, telefono, correo, id=None):
        self.id = id
        self.nombre = nombre
        self.documento = documento  
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo

    
    def __str__(self):
        return f"{self.nombre} ({self.documento})"