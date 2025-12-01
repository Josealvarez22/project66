
class Venta:
    def __init__(self, nro_contrato, fecha, forma_pago, cuotas, impuestos, garantia, id_cliente, id_vehiculo, id=None):
        self.id = id
        self.nro_contrato = nro_contrato
        self.fecha = fecha
        self.forma_pago = forma_pago 
        self.cuotas = cuotas
        self.impuestos = impuestos
        self.garantia = garantia
        self.id_cliente = id_cliente
        self.id_vehiculo = id_vehiculo