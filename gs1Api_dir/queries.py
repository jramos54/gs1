import pyodbc

def fetch_atributos(connection_string):
    with pyodbc.connect(connection_string) as conn:
        cursor = conn.cursor()
        query = "SELECT Atributo_Descripcion FROM TAtributos_GS1"
        cursor.execute(query)

        results = cursor.fetchall()

    return [row[0] for row in results]

def write_atributos_sqlserver(atributos_nuevos, connection_string):
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    try:
        for atributo_nombre in atributos_nuevos:
            # Intenta insertar cada atributo nuevo
            try:
                cursor.execute("INSERT INTO TAtributos_GS1 (Atributo_Descripcion) VALUES (?)", atributo_nombre)
            except pyodbc.Error as e:
                print(f"Error al insertar '{atributo_nombre}': {e}")

        conn.commit()
    finally:
        cursor.close()
        conn.close()
        
def fetch_atributo_id(connection_string, atributo_nombre):
    with pyodbc.connect(connection_string) as conn:
        cursor = conn.cursor()
        # Asegúrate de proteger contra inyecciones SQL. No concatenes directamente la entrada del usuario a la consulta.
        query = "SELECT PkAtributo FROM TAtributos_GS1 WHERE Atributo_Descripcion = ?"
        cursor.execute(query, (atributo_nombre,))

        result = cursor.fetchone()

    return result[0] if result else None

def write_producto_sqlserver(GTIN, id_atributo, valor_atributo, connection_string):

    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # Verificar si el producto ya existe
    cursor.execute("SELECT PkAtributoValor FROM TAtributosProductos_GS1 WHERE CodigoBarras = ? AND FkAtributo = ?", GTIN, id_atributo)
    data = cursor.fetchone()

    if not data:
        # Insertar el producto si no existe
        cursor.execute("INSERT INTO TAtributosProductos_GS1 (CodigoBarras, FkAtributo, Valor_Atributo) VALUES (?, ?, ?)", GTIN, id_atributo, valor_atributo)
        conn.commit()
        print(f"Producto con GTIN {GTIN} y atributo {id_atributo} agregado con éxito.")
    
    cursor.close()
    conn.close()
    
def write_productos_batch(productos, connection_string):
    print("\t\t\tINSERTION TO DB")
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    gtins_unicos = set(producto[0] for producto in productos)

    productos_existentes = {}
    if gtins_unicos:  # Asegurarse de que la lista no esté vacía
        placeholders = ', '.join('?' for _ in gtins_unicos)
        query = f"SELECT CodigoBarras, FkAtributo FROM TAtributosProductos_GS1 WHERE CodigoBarras IN ({placeholders})"
        cursor.execute(query, list(gtins_unicos))
        for row in cursor.fetchall():
            productos_existentes[(row.CodigoBarras, row.FkAtributo)] = True

    insertar_productos = []

    for producto in productos:
        GTIN, id_atributo, valor_atributo = producto

        if not productos_existentes.get((GTIN, id_atributo)):
            insertar_productos.append((GTIN, id_atributo, valor_atributo))
            print(f"to insert {GTIN} - {id_atributo} - {valor_atributo}")

    if insertar_productos:
        print("WRITTING IN DB")
        cursor.executemany("INSERT INTO TAtributosProductos_GS1 (CodigoBarras, FkAtributo, Valor_Atributo) VALUES (?, ?, ?)", insertar_productos)
        conn.commit()

    cursor.close()
    conn.close()


def getGtin(connection):
    
    conn = pyodbc.connect(connection)
    cursor = conn.cursor()

    try:
        # Ejecutar la consulta
        cursor.execute("SELECT DISTINCT CodigoBarras FROM TAtributosProductos_Gs1")

        # Recuperar todos los resultados
        items = cursor.fetchall()

        # Convertir la lista de tuplas a una lista simple
        items = [item[0] for item in items]

        return items

    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return []

    finally:
        # Cerrar la conexión a la base de datos
        conn.close()

def load_atributes(connection):
    # Esta función carga todos los atributos y sus IDs de la base de datos
    # y los almacena en un diccionario.
    atributos_dict = {}
    conn = pyodbc.connect(connection)
    cursor = conn.cursor()
    cursor.execute("SELECT Atributo_Descripcion,PkAtributo FROM TAtributos_GS1")  # Asegúrate de ajustar esta consulta
    for key, id_atributo in cursor.fetchall():
        atributos_dict[key] = id_atributo
    return atributos_dict