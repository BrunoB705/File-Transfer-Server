import uuid
import os
import shutil
from fastapi import HTTPException
from app.database.file_repository import get_file_by_id, delete_file
from datetime import datetime

#ACA VA LA LOGICA DEL NEGOCIO


def save_file(file):
    """
      Guarda un archivo en el sistema de almacenamiento y devuelve información del archivo.
      
      Returns:
          dict con 'stored_name' (nombre interno), 'original_name', 'size'
    """
    try:
        os.makedirs("storage",exist_ok=True)

        file_extension = os.path.splitext(file.filename)[1]
        file_id = str(uuid.uuid4())
        unique_filename = f"{file_id}{file_extension}"

        file_path = os.path.join("storage",unique_filename)

        # tamaño
        file.file.seek(0, 2)
        size = file.file.tell()
        file.file.seek(0)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "id": file_id,
            "original_name": file.filename,
            "stored_name": unique_filename,
            "size": size,
            "upload_date": datetime.now().strftime("%d/%m/%Y")  # Formato fecha legible
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar el archivo: {str(e)}")
    
def download_file(file_id):
    file_data = get_file_by_id(file_id)

    if not file_data:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    
    with open(f"storage/{file_data['stored_name']}", "rb") as f:
        return {"content": f.read(),
                "filename": file_data["original_name"],  # Clave que usa el endpoint
                "size": file_data["size"]}

def delete_file_by_id(file_id):
    file_data = get_file_by_id(file_id)

    if not file_data:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    #Borra de la carpeta storage
    os.remove(f"storage/{file_data['stored_name']}")
    delete_file(file_id)