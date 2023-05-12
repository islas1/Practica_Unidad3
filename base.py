import sqlite3

conexion=sqlite3.connect("crud.db")

conexion.execute("""create table if not exists personas(
                    id integer primary key AUTOINCREMENT,
                    nombre varchar,
                    contraseña varchar
                    )""")
conexion.close()

import random
for i in range(10): 
    num = random.randint(9999,99999)
conexion = sqlite3.connect("crud.db")
nombrejugador= str(input("Ingresa un nombre: --> "))
contrajugador= str(input("Ingresa una contraseña: --> "))
conexion.execute("Insert into personas(id,nombre,contraseña) values(?,?,?)", (num,nombrejugador,contrajugador))
conexion.commit()
juga = conexion.execute("select * from personas where nombre = ?", (nombrejugador, ))
fila = juga.fetchone()

print(fila)

conexion.close()