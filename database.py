import pymysql


conexion=pymysql.connect(
            host='localhost',    
            user='root',         
            password='Robin#707+', 
            database='ecommercedb',
            cursorclass=pymysql.cursors.DictCursor 
        )
print("Conexión exitosa a MySQL")

