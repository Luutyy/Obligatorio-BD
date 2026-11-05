import mysql.connector

conexion = mysql.connector.connect(
    host='localhost',
    user='root',
    password='rootpassword',
    database='torneo',
    port=3306
)

if conexion.is_connected():
    print('conectado a la base de datos')