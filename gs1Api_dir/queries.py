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