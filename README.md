# Mini Cloud - Servidor de Transferencia Local

API RESTful simple para subir y descargar archivos localmente usando FastAPI + SQLite.

---

## Características

- Subir archivos con UUID único por archivo (evita colisiones)
- Listar todos los archivos almacenados
- Descargar archivos por ID de referencia
- Base de datos SQLite persistente para metadatos
- Documentación interactiva con Swagger UI
- Arquitectura escalable en 4 capas

---

## Estructura del Proyecto

```
Mini Cloud/
├── app/                    # Núcleo de la aplicación
│   ├── main.py            # FastAPI entrypoint
│   ├── routes/            # Endpoints HTTP (recepción)
│   │   └── files.py       # POST /upload, GET /list, GET /download
│   ├── services/          # Lógica de negocio
│   │   └── file_service.py# Genera UUID, guarda archivos físicos
│   ├── database/          # Persistencia SQLite
│   │   ├── connection.py  # Inicializa tabla 'files'
│   │   └── repository.py  # CRUD sobre metadatos
│   ├── core/              # Configuración 
│   └── models/            # Pydantic models 
├── storage/               # Almacenamiento físico de archivos
├── tests/                 # Tests unitarios 
├── requirements.txt       # Dependencias Python
└── README.md              # Esta documentación
```

---

## Instalación y Ejecución

### 1. Clonar repositorio
```bash
git clone <TU_REPO>
cd Mini Cloud
```

### 2. Activar entorno virtual (Windows)
```powershell
venv\Scripts\Activate.ps1
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Iniciar servidor
```bash
python -m uvicorn app.main:app --reload --port 8000
```

---

## 📡 Endpoints Disponibles

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/files/upload` | Sube archivo, devuelve ID único |
| GET | `/files/list` | Lista todos los archivos en DB |
| GET | `/download/{id}` | Descarga archivo por UUID |

---

## Ejemplos de Uso

### curl - Sin autenticación (actualmente abierto)
```bash
# Listar archivos
curl http://localhost:8000/files/list

# Subir archivo
curl -X POST -F "file=@pathfile" \
  http://localhost:8000/files/upload

# Descargar por ID 
curl http://localhost:8000/download/uuid -o filename
```

### Swagger UI (documentación interactiva)
Abre en navegador: `http://localhost:8000/docs`

---

##  Acceso desde Celular (LAN Local)

1. Encuentra tu IP de PC:
   ```powershell
   ipconfig | findstr "IPv4"
   # Ejemplo: 192.168.1.XXX
   ```

2. Inicia servidor para LAN:
   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

3. Desde celular (misma red WiFi):
   ```
   http://TU_IP_AQUI:8000/docs
   ```

**Importante**: Solo funciona en la misma red local (LAN).

---

##  Base de Datos - Estructura

Tabla `files`:
```sql
id TEXT PRIMARY KEY              -- UUID v4 generado por el servicio
original_name TEXT NOT NULL      -- Nombre original del archivo subido  
stored_name TEXT NOT NULL        -- UUID + extensión (ej: a8f3d2.pdf)
size INTEGER NOT NULL            -- Tamaño en bytes
upload_date TEXT NOT NULL        -- Fecha de subida ("02/05/2026")
```

---

## Arquitectura - 4 Capas

1. **HTTP Layer** (`routes/`) → Recibe requests, valida inputs básicos
2. **Services Layer** (`services/`) → Lógica: genera UUID, guarda archivos físicos  
3. **Database Layer** (`database/`) → SQLite: persistencia de metadatos
4. **Storage Layer** (`storage/`) → Filesystem: almacenamiento físico


---

##  Notas Importantes

- No hay autenticación actualmente
- Archivos se guardan con UUID + extensión original (evita colisiones de nombres)
- Base de datos SQLite en raíz del proyecto (`database.db`)
