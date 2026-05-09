from fastapi import APIRouter, File, UploadFile, HTTPException
from starlette.responses import StreamingResponse
from app.services.file_service import save_file, download_file, delete_file_by_id
from app.database.connection import init_db
from app.database.file_repository import insert_file, get_all_files

# Inicializar DB al importar
init_db()

def convertir_bytes(tamaño_bytes):
    return f"{tamaño_bytes/(1024**2):.2f} MB"

router = APIRouter()

@router.post("/files/upload")
async def upload_file(file: UploadFile = File(...)):
    """Sube archivo"""
    
    # Validar tamaño maximo de 100MB
    if file.size > 100*1024*1024:
        raise HTTPException(status_code=413, detail="El archivo no puede superar los 100MB")
    
    file_info = save_file(file)
    insert_file(file_info)
    return {"message": "Archivo subido correctamente.", "id": file_info["id"]}

@router.get("/files/list")  
async def list_files():
    """Lista todos los archivos"""
    files = get_all_files()
    return [{
         "id":f["id"],
         "original_name":f["original_name"],
         "size": convertir_bytes(f["size"]),
         "upload_date":f["upload_date"]
    }
        for f in files
    ]


@router.get("/download/{file_id}")
async def download(file_id: str):
    """Descarga archivo por ID"""
    
    # Usar función del servicio para obtener datos (no llama a database directamente)
    file_data = download_file(file_id)
    
    # Devolver con StreamingResponse (FileResponse no acepta 'content')
    return StreamingResponse(
        iter([file_data["content"]]), 
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{file_data["filename"]}"'}
    )

@router.delete("/files/{file_id}")
async def delete(file_id: str):
        """"Elimina un archivo por ID"""

        delete_file_by_id(file_id)
        return{"Message":"Archivo eliminado correctamente."}

