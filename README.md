# Pet Manager Python

Aplicación de escritorio Tkinter para administrar perros y gatos, consultar reportes por estado de salud y exportar listados a Excel.

## Requisitos

- Python
- MySQL con la base `administracionmascotasbd` y las tablas `tb_pet`, `tb_dog` y `tb_cat`
- Tkinter disponible en la instalación de Python

## Instalación y ejecución

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python View/frmPet.py
```

La conexión usa por defecto `localhost:3306`, el usuario `root` y la base `administracionmascotasbd`. Se puede configurar mediante `PET_DB_HOST`, `PET_DB_PORT`, `PET_DB_NAME`, `PET_DB_USER` y `PET_DB_PASSWORD`.
