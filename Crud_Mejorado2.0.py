from tkinter import *
import tkinter as tk
from tkinter import messagebox
import mysql.connector
import sqlite3

conexion = sqlite3.connect("crud.db")

def validacion(valor):
    pichula = conexion.execute("select nombre from personas where nombre = ?", (valor, ))
    valid = False
    valid2 = True
    # El método fechone de la clase Cursor retorna una tupla con la fila de la tabla que coincide con el código ingresado o retorna 'None':
    fila= pichula.fetchone()
    if fila == None :
        messagebox.showerror("Dato erroneo","El servicio ingresado no es válido")
    else:
         print("aqui todo bien")
         valid= True
         return valid

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="escuela"
    )
except mysql.connector.Error as e:
    messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {e}")
    exit()

# Tabla de usuarios ( dice alumnos por que es del codigo de la maestra)
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS alumnos (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(255), edad INT, email VARCHAR(255))")

# Función para leer todos los alumnos de la base de datos
def leer_datos_usuario():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM alumnos")
    return cursor.fetchall()

# borra xd
def eliminar_usuario(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM alumnos WHERE id = %s", (id,))
    db.commit()

# agrega a la base al nuevo jugador
def agregar_nuevo_usuario(nombre, edad, email):
    try:
        cursor = db.cursor()
        cursor.execute("INSERT INTO alumnos (nombre, edad, email) VALUES (%s, %s, %s)", (nombre, edad, email))
        db.commit()
    except mysql.connector.Error as error:
        messagebox.showerror("Error al agregar al usuario", f"No se pudo agregar al jugador: {error}")
    finally:
        cursor.close()

# actualiza
# El %s representa el valor de la base de datos
def actualizar_usuario_existente(id, nombre, edad, email):
    iid = int(id)
    cursor = db.cursor()
    print("UPDATE alumnos SET nombre = %s, edad = %s, email = %s WHERE id = %s", (nombre, edad, email, iid))
    cursor.execute("UPDATE alumnos SET nombre = %s, edad = %s, email = %s WHERE id = %s", (nombre, edad, email, iid))
    db.commit()

# muestra los datod ingresados en la base de datos
def mostrar_datos_ingresados():
    # Limpiar la tabla
    # El .winfo_children devuelve una lista que contiene los nombres de ruta de todos los elementos secundarios de la ventana. Las ventanas de nivel superior se devuelven como hijos de sus padres lógicos.
    for widget in tabla_usuarios.winfo_children():
        widget.destroy()

    # Obtener todos los alumnos
    usuarios = leer_datos_usuario()

    # Mostrar los alumnos en la tabla
    for i, usuario in enumerate(usuarios):
        id = usuario[0]
        nombre = usuario[1]
        edad = usuario[2]   
        email = usuario[3]

        Label(tabla_usuarios,bg="paleturquoise", text=id).grid(row=i, column=0)
        Label(tabla_usuarios,bg="paleturquoise", text=nombre).grid(row=i, column=1)
        Label(tabla_usuarios,bg="paleturquoise", text=edad).grid(row=i, column=2)
        Label(tabla_usuarios,bg="paleturquoise", text=email).grid(row=i, column=3)
    
def ingresar_usuario():
    # datos del nuevo jugador
    nombre = entrada_nombre.get()  
    edad = entrada_edad.get()
    email = entrada_email.get()

    # Validar que los campos no estén vacíos
    if not nombre or not edad or not email:
        messagebox.showerror("Error al agregar al jugador", "Por favor ingrese todos los datos del jugador")
        return

    # Agregar el nuevo jugador
    agregar_nuevo_usuario(nombre, edad, email)

    # Limpia las entradas de datos
    entrada_nombre.delete(0, END)
    entrada_edad.delete(0, END)
    entrada_email.delete(0, END)

    # nueva lista de jugadores
    mostrar_datos_ingresados()

def eliminar_usuarioprincipal():
    # Obtener el ID del alumno a eliminar
    id = entrada_id.get()

    # Validar que se haya ingresado un ID
    if not id:
        messagebox.showerror("Error al eliminar al Jugador", "Por favor ingrese el ID del jugador a eliminar")
        return

    # Preguntar al usuario si está seguro de eliminar el alumno
    confirmar = messagebox.askyesno("Confirmar eliminación", "¿Está seguro de eliminar este jugador?")

    if confirmar:   
        # Eliminar el alumno
        eliminar_usuario(id)

        # Limpiar los campos de entrada
        entrada_id.delete(0, END)
        entrada_nombre.delete(0, END)
        entrada_edad.delete(0, END)
        entrada_email.delete(0, END)

        # Mostrar la lista actualizada de alumnos
        mostrar_datos_ingresados()

def actualizar_usuarioprincipal():
    
    nombre = entrada_nombre.get()
    edad = entrada_edad.get()
    email = entrada_email.get()
    id = entrada_id.get()

    # Validar que los campos no estén vacíos
    if not id or not nombre or not edad or not email:
        messagebox.showerror("Error al actualizar al jugador", "Por favor ingrese todos los datos del jugador")
        return

    # Actualizar el jugador
    actualizar_usuario_existente(id, nombre, edad, email)

    # Limpiar los campos de entrada
    entrada_id.delete(0, END)
    entrada_nombre.delete(0, END)
    entrada_edad.delete(0, END)
    entrada_email.delete(0, END)

    # Mostrar la lista actualizada de jugadores
    mostrar_datos_ingresados()

def creación_cuenta():
    ventana10 = tk.Tk()
    ventana10.title("crear cuenta")
    ventana10.geometry("500x400")
    ventana10.config(bg="paleturquoise")
    ventana10.resizable(width=False, height=False)
    conexion = sqlite3.connect("crud.db")
    conexion.execute("""create table if not exists personas(
                    id integer primary key AUTOINCREMENT,
                    nombre varchar,
                    contraseña varchar
                    )""")
    conexion.close
    marco = LabelFrame(ventana10, text="Datos para crear la cuenta", font=("Comic Sans", 10, "bold"), bg="paleturquoise")
    marco.config(bd=2,pady=5)
    marco.pack()
    # Crear la etiqueta y el campo de entrada de los datos
    persona = tk.Label(marco,text="datos del ciente", bg="paleturquoise", font=("Comic Sans", 10, "bold"))
    persona.grid(row=0, column=0, padx=(10, 0))
    "---------------edad-------------"
    contra_label = tk.Label(marco, text="contraseña:", bg="paleturquoise", font=("Comic Sans", 10, "bold"))
    contra_label.grid(row=1, column=0, padx=(10, 0))
    contra_entry = tk.Entry(marco)
    contra_entry.grid(row=1, column=1,sticky='s', padx=(0, 10), pady=(10, 0))
    "-------------nombre-------------"
    name_label = tk.Label(marco, text="Nombre :", bg="paleturquoise", font=("Comic Sans", 10, "bold"))
    name_label.grid(row=2, column=0, padx=(10, 0))
    name_entry = tk.Entry(marco)
    name_entry.grid(row=2, column=1, sticky='s', padx=(0, 10), pady=(10, 0))

    submit_button = tk.Button(marco, text="siguiente", bg="Light cyan", command=ventana10.destroy)
    submit_button.grid(row=7, column=0, columnspan=2, pady=10, padx=10)

    global name
    name = name_entry
    global contra
    contra = contra_entry
    iddd = "102839"
    namestr = str(name.get())
    contrastr = str(contra.get())
    global nameee
    nameee = namestr
    conexion = sqlite3.connect("crud.db")
    conexion.execute("Insert into personas(nombre,contraseña) values(?,?)", (namestr,contrastr))
    conexion.commit()
    prueba_BASE = str(namestr)
    pichula = conexion.execute("select nombre from personas where nombre = ?", (prueba_BASE, ))
    fila = pichula.fetchone()
    global filaaaaa
    filaaaaa = fila
    conexion.close
    ventana10.mainloop

def login777():
    def comprobacion():
        name4 = str(name3.get())
        contra4 = str(contra3.get())
        variable = str(validacion(name4))
        if variable != True :
            messagebox.showerror("Dato erroneo","Alguno de los datos no es correcto")
        elif variable == True :
            ventana = Tk()
            ventana.configure(bg="paleturquoise")
            ventana.configure(padx=80)
            ventana.configure(pady=50)
            ventana.title("Practica1_CRUD") 

            # Crear los campos de entrada para los datos del alumno
            Label(ventana,bg="paleturquoise", text="Id:").grid(row=0, column=0, padx=5, pady=5)
            entrada1_id = Entry(ventana)
            entrada1_id.grid(row=0, column=1, padx=5, pady=5)

            Label(ventana,bg="paleturquoise", text="Nombre:").grid(row=1, column=0, padx=5, pady=5)
            entrada1_nombre = Entry(ventana)
            entrada1_nombre.grid(row=1, column=1, padx=5, pady=5)

            Label(ventana,bg="paleturquoise", text="Edad:").grid(row=0, column=2, padx=5, pady=5)
            entrada1_edad = Entry(ventana)
            entrada1_edad.grid(row=0, column=3, padx=5, pady=5)

            Label(ventana,bg="paleturquoise", text="Email:").grid(row=1, column=2, padx=5, pady=5)
            entrada1_email = Entry(ventana)
            entrada1_email.grid(row=1, column=3, padx=5, pady=5)

            # Crear los botones para agregar, actualizar y eliminar alumnos
            Button(ventana,bg="beige", text="Agregar alumno", command=ingresar_usuario).grid(row=7, column=3, padx=12, pady=10)
            Button(ventana, text="Actualizar alumno", command=actualizar_usuarioprincipal).grid(row=7, column=2, padx=8, pady=8)
            Button(ventana, text="Eliminar alumno", command=eliminar_usuarioprincipal).grid(row=7, column=1, padx=8, pady=6)

            # Crear la tabla para mostrar los alumnos
            tabla_usuarios1 = Frame(ventana,bg="paleturquoise",)
            tabla_usuarios1.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

            Label(tabla_usuarios1,bg="paleturquoise", text="ID").grid(row=0, column=0)
            Label(tabla_usuarios1,bg="paleturquoise", text="Nombre").grid(row=0, column=1)
            Label(tabla_usuarios1,bg="paleturquoise", text="Edad").grid(row=0, column=2)
            Label(tabla_usuarios1,bg="paleturquoise", text="Email").grid(row=0, column=3)

            global entrada_nombre
            entrada_nombre = entrada1_nombre
            global entrada_id
            entrada_id = entrada1_id
            global entrada_edad
            entrada_edad = entrada1_edad
            global entrada_email
            entrada_email = entrada1_email
            global tabla_usuarios
            tabla_usuarios = tabla_usuarios1



            # Mostrar la lista de alumnos en la tabla
            mostrar_datos_ingresados()

    ventana2 = tk.Tk()
    ventana2.resizable(width=False, height=False)
    ventana2.configure(background="paleturquoise")
    #ventana2.iconbitmap("pet.ico")
    ventana2.title("Login ")
    ventana2.configure(padx=165)
    ventana2.configure(pady=20)
    # Entrada para la contraseña
    print("aqui debe mostrar nameeee")
    marco = LabelFrame(ventana2, text="Datos del usuario", font=("Comic Sans", 10, "bold"), bg="paleturquoise")
    marco.config(bd=2,pady=5)
    marco.pack()
    # Crear la etiqueta y el campo de entrada de los datos
    persona = tk.Label(marco,text="datos del ciente", bg="paleturquoise", font=("Comic Sans", 10, "bold"))
    persona.grid(row=0, column=0, padx=(10, 0))
    "---------------edad-------------"
    contra_label = tk.Label(marco, text="contraseña:", bg="paleturquoise", font=("Comic Sans", 10, "bold"))
    contra_label.grid(row=1, column=0, padx=(10, 0))
    contra_entry = tk.Entry(marco)
    contra_entry.grid(row=1, column=1,sticky='s', padx=(0, 10), pady=(10, 0))
    "-------------nombre-------------"
    name_label = tk.Label(marco, text="Nombre :", bg="paleturquoise", font=("Comic Sans", 10, "bold"))
    name_label.grid(row=2, column=0, padx=(10, 0))
    name_entry = tk.Entry(marco)
    name_entry.grid(row=2, column=1, sticky='s', padx=(0, 10), pady=(10, 0))

    submit_button = tk.Button(marco, text="Guardar e iniciar sesión", bg="Light cyan", command=comprobacion)
    submit_button.grid(row=7, column=0, columnspan=2, pady=10, padx=10)

    global name3
    name3 = name_entry
    global contra3
    contra3 = contra_entry

ventanaprincipal = Tk()
ventanaprincipal.configure(bg="paleturquoise")
ventanaprincipal.configure(padx=80)
ventanaprincipal.configure(pady=100)
ventanaprincipal.title("Game world")
tK =tk.Label(ventanaprincipal, text=" Bienvenido a GameWorld ", bg="paleturquoise",
          fg="black", width="20", height="1", font=("Bahnschrift", 15)).grid()
Iniciar_Sesion1 =  tk.Button(ventanaprincipal, text="Iniciar Sesión",bg="beige",command=login777)  
Iniciar_Sesion1.grid(padx=20, pady=20)

ventanaprincipal.mainloop()