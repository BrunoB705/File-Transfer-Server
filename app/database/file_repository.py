import sqlite3
from app.database.connection import get_db_connection
from fastapi import HTTPException

#Map de uso global
field_map = ['id','original_name','stored_name','size','upload_date']


def insert_file(file_data):
    """Inserta datos de un archivo en la base de datos."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO files (id, original_name, stored_name, size, upload_date)
            VALUES (?, ?, ?, ?, ?)""", (
                file_data["id"],
                file_data["original_name"],
                file_data["stored_name"],
                file_data["size"],
                file_data["upload_date"]))
        
        conn.commit()

def get_all_files():
    """Lista todos los registros de la tabla"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM files")
            files_list = []
            for row in cursor.fetchall():
                file_dict = {field : value for field, value in zip(field_map, row)}
                files_list.append(file_dict)
            return files_list
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

def get_file_by_id(file_id):
    """Obtiene un archivo por su ID."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM files WHERE id = ?", (file_id,))
            row = cursor.fetchone()

            if not row:
                return None
            return {field: value for field, value in zip(field_map,row)}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

def delete_file(file_id):
    """Elimina un archivo de la base de datos."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM files WHERE id = ?", (file_id,))
        conn.commit()
