import psycopg2

class Database:
    SERVIDOR = 'localhost'
    BASE_DATOS = 'kinoscope_bd'
    USUARIO = 'postgres'
    CONTRASEÑA = 'Patata12'
    PORT = 5432
    CONNECTION_STR = None
    conn = None # Conexión a la BD
    cursor = None # Objeto cursor utilizado para realizar las consultas
    
    # Constructor
    def __init__(self) -> None:
        self.CONNECTION_STR = "dbname={0} user={1} password={2} host={3} port={4}".format(
            self.BASE_DATOS, self.USUARIO, self.CONTRASEÑA, self.SERVIDOR, self.PORT
        )
    
    def open_connection(self) -> None:
        self.conn = psycopg2.connect(self.CONNECTION_STR)
    
    def close_connection(self) -> None:
        self.conn.close()
    
    # Método utilizado para ejecutar consultas que regresan resultados (SELECT)
    def execute_query_return(self, sql:str) -> object:
        self.open_connection()
        self.cursor = self.conn.cursor()
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.conn.commit() # Terminar transacción
        self.close_connection()
        return resultado
    
    # Método utilizado para ejecutar consultas que no regresan resultados (INSERT, UPDATE, DELETE)
    def execute_query(self, sql:str) -> None:
        self.open_connection()
        self.cursor = self.conn.cursor()
        resultado = self.cursor.execute(sql)
        self.conn.commit()  # Terminar transacción
        self.close_connection()
