import pymysql

conexion=pymysql.connect(
        host="host.docker.internal", # Cambiar a localhost para poder realizar las pruebas unitarias de forma local
        user='root',
        password='Robin#707+',
        database='ecommercedb',
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True  
    )

print("conexion exitosa a mysql")