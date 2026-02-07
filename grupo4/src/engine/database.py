#aqui es donde va la conexión con la base de datos.
from sqlalchemy import create_engine
db_connection = create_engine("mysql+mysqldb://root:-@localhost:3306/expertsystems",
    pool_recycle=3000, echo=True
)

#Hacer clases
#Database connection
#Hacer CRUD de las especies de porcelanidos.
#
#

class DB:
    def __init__(self, user, password, url, port):
        self.user = user
        self.password = password
        self.url = url
        self.port = port