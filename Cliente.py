from json import JSONEncoder

class Cliente:
    
    def __init__(self, id_cliente:str, nombre:str, apellido_paterno:str, apellido_materno:str,
                 email:str, contraseña:str, telefono:str, datos_de_pago:dict):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.email = email
        self.contraseña = contraseña
        self.telefono = telefono
        self.datos_de_pago = datos_de_pago
    
class ClienteEncoder(JSONEncoder):
    '''
        Esta clase se utiliza para la serialización/deserialización JSON.
            * Se obtiene el resultado de una query como JSON -> Se transforma a Cliente
            * Se tiene un objeto Cliente -> Se transforma a JSON
    '''
    def default(self, o):
        return o.__dict__
