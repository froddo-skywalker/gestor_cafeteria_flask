from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf.csrf import CSRFProtect

# Extensiones desacopladas de la instancia Flask.
db = SQLAlchemy()
server_session = Session()
csrf = CSRFProtect()
