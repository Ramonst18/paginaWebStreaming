from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, inspect
from tablas import Base
db = SQLAlchemy()

def iniciar_bd(app, cadenapsql):
    """Iniciador de la base de datos"""
    db.init_app(app)
    engine = create_engine(cadenapsql)
    print("Se inició la base de datos")
    return engine

def crear_bd(app, engine):
    inspeccionar = inspect(engine)
    if (not inspeccionar.has_table("peliculas", schema="dbo")):
        app.app_context().push()
        Base.metadata.create_all(engine)
        print("Tablas creadas")