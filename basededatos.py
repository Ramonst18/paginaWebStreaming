from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, inspect
db = SQLAlchemy()

def iniciar_bd(app, cadenapsql):
    """Iniciador de la base de datos"""
    db.init_app(app)
    engine = create_engine(cadenapsql)
    print("Se inició la base de datos")
    return engine
