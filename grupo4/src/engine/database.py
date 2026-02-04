#aqui es donde va la conexión con la base de datos.
from sqlalchemy import create_engine
db_connection = create_engine("mysql+mysqldb://admin:password@localhost:3306/expertsystems",
    pool_recycle=3000, echo=True
)

#Hacer clases
#Database connection
#
