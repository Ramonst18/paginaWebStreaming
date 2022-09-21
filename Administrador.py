from json import JSONEncoder

class Administrador():
    # Constructor
    def __init__(self, id_admin:int, nombre:str, apellido_paterno:str, apellido_materno:str, contraseña:str):
        self.id_admin = id_admin
        self.nombre = nombre
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.contraseña = contraseña
        
class AdministradorEncoder(JSONEncoder):
    '''
        Esta clase se utiliza para la serialización/deserialización JSON.
            * Se obtiene el resultado de una query como JSON -> Se transforma a Administrador
            * Se tiene un objeto Administrador -> Se transforma a JSON
    '''
    def default(self, o):
        return o.__dict__