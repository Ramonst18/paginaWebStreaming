from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
Base = declarative_base()

class Peliculas(Base):
    """Contiene toda la estructura para poder mandar informacion
    a la tabla Peliculas de la base de datos"""
    __tablename__ = "peliculas"
    
    #Atributos de clase
    id_pelicula = Column(Integer, primary_key=True)
    titulo = Column(String(255), nullable=False)
    año = Column(Integer)
    director = Column(String(128))
    genero = Column(String(128))
    duracion = Column(Integer)
    elenco = Column(JSON)
    calif_imbd = Column(Float(4))
    pais = Column(String(32))
    clasif_por_edad = Column(String(32))
    sinopsis = Column(String)
    poster = Column(String)
    stream_video = Column(String)
    fecha_agregada = Column(String(10))
    visualizaciones = Column(Integer)
    tipo_contenido = Column(String)
    
    def __init__(self, titulo, anio, director, genero, duracion, elenco, calif_imbd, pais, clasif_edad, sinopsis, poster, Tcontenido):
        #Damos la data d:
        self.titulo = titulo
        self.año = anio
        self.director = director
        self.genero = genero
        self.duracion = duracion
        self.elenco = elenco
        self.calif_imbd = calif_imbd
        self.pais = pais
        self.clasif_por_edad = clasif_edad
        self.sinopsis = sinopsis
        self.poster = poster
        self.tipo_contenido = Tcontenido
        
        #Atributos sin saber que pedo
        self.fecha_agregada = "a"
        self.visualizaciones = 0
        self.stream_video = "a"
    
    def __repr__(self):
        return '<id {}>'.format(self.id_pelicula)