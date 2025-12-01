
class Vehiculo:
    def __init__(self, marca, modelo, anio, vin, motor, color, precio, estado="nuevo", id=None):
        self.id = id
        self.marca = marca
        self.modelo = modelo
        self.anio = anio
        self.vin = vin
        self.motor = motor
        self.color = color
        self.precio = precio
        self.estado = estado