import sqlite3

def check_database():
    try:
        conn = sqlite3.connect('scraped_data.db')
        cursor = conn.cursor()

        # Listar todas las tablas en la base de datos
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if tables:
            print("Tablas en la base de datos:")
            for table in tables:
                print(table[0])
                # Mostrar la estructura de cada tabla
                cursor.execute(f"PRAGMA table_info({table[0]})")
                columns = cursor.fetchall()
                print("Columnas:")
                for column in columns:
                    print(f"  {column[1]} - {column[2]}")
        else:
            print("La base de datos no contiene tablas.")

        conn.close()
    except sqlite3.Error as e:
        print(f"Error al acceder a la base de datos: {e}")

if __name__ == "__main__":
    check_database()