from json import JSONEncoder


class Pelicula():
    # Constructor
    def __init__(self, id_pelicula: int, titulo: str, año: int, director: str, genero: str, duracion: int,
                 elenco: str, calif_imdb: float, pais: str, clasif_por_edad: str, sinopsis: str, poster: str,
                 stream_video: str, fecha_agregada: str, visualizaciones: int, tipo_contenido: str):
        self.id_pelicula = id_pelicula
        self.titulo = titulo
        self.año = año
        self.director = director
        self.genero = genero
        self.duracion = duracion
        self.elenco = elenco
        self.calif_imdb = calif_imdb
        self.pais = pais
        self.clasif_por_edad = clasif_por_edad
        self.sinopsis = sinopsis
        self.poster = poster
        self.stream_video = stream_video
        self.fecha_agregada = fecha_agregada
        self.visualizaciones = visualizaciones
        self.tipo_contenido = tipo_contenido


class PeliculaEncoder(JSONEncoder):
    '''
        Esta clase se utiliza para la serialización/deserialización JSON.
            * Se obtiene el resultado de una query como JSON -> Se transforma a Pelicula
            * Se tiene un objeto Pelicula -> Se transforma a JSON
    '''

    def default(self, o):
        return o.__dict__
