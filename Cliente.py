class Cliente:
    
    def __init__(self, id_cliente, nombre, apellido_paterno, apellido_materno, email, contraseña, telefono, datos_de_pago):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.email = email
        self.contraseña = contraseña
        self.telefono = telefono
        if datos_de_pago is None:
            self.datos_de_pago = dict()
        else:
            #faltante
            print()