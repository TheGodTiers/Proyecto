import pymysql

conexion=pymysql.connect(
        host="host.docker.internal",
        user='root',
        password='Robin#707+',
        database='ecommercedb',
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True  
    )

print("conexion exitosa a mysql")