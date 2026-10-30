# Gestor de Cafetería Modular

## Requisitos
- Python 3.10 o superior
- pip

## Instalación (Windows PowerShell)
```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
py run.py
```

## Instalación (macOS / Linux)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python run.py
```

Abre http://127.0.0.1:5000

## Acceso de demostración
- Freddy Colina / 12345678*
- David Reyes / 12345678*

Las claves se guardan en la base de datos como hashes. Cambia las credenciales y `SECRET_KEY` antes de cualquier despliegue real.

## Funcionalidades
- Catálogo público por categorías.
- Carrito con sesiones guardadas en el servidor (Flask-Session filesystem).
- Checkout y comprobante digital.
- Login administrativo y cierre de sesión.
- Dashboard con pedidos recientes y cambio de estado.
- Registro de pedidos de salón con número de mesa.
- SQLite y modelos ORM con relaciones.
- Protección CSRF en formularios POST.
- Interfaz Bootstrap 5 sin JavaScript.

## Base de datos
Se crea automáticamente en `instance/cafeteria.sqlite3`. Los administradores y platos de muestra se insertan automáticamente si no existen.

Para reiniciar los datos de demostración, detén el servidor y elimina `instance/cafeteria.sqlite3` y la carpeta `instance/flask_session`. Al volver a iniciar, se reconstruyen.

## Estructura
```text
gestor_cafeteria_modular/
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   ├── utils.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── usuario.py
│   │   ├── plato.py
│   │   ├── pedido.py
│   │   └── detalle_pedido.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── public.py
│   │   └── admin.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── 404.html
│   │   ├── public/
│   │   └── admin/
│   └── static/css/styles.css
├── instance/                 # Se crea al ejecutar
├── .env.example
├── requirements.txt
├── README.md
└── run.py
```

## Nota de producción
Este es un proyecto académico listo para desarrollo local. Antes de desplegarlo: configura una `SECRET_KEY` segura, HTTPS y `SESSION_COOKIE_SECURE=True`; cambia las claves iniciales; utiliza un servidor WSGI de producción y define políticas de respaldo de SQLite.
