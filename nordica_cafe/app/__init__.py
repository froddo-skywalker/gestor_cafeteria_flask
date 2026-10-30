import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, render_template

from .extensions import db, server_session, csrf

def create_app(test_config=None):
    """Fábrica de aplicaciones: configura extensiones, rutas y datos iniciales."""
    load_dotenv()
    app = Flask(__name__, instance_relative_config=True)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    session_dir = Path(app.instance_path) / "flask_session"
    session_dir.mkdir(parents=True, exist_ok=True)

    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "clave-local-solo-para-desarrollo"),
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{Path(app.instance_path) / 'cafeteria.sqlite3'}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SESSION_TYPE="filesystem",
        SESSION_FILE_DIR=str(session_dir),
        SESSION_PERMANENT=False,
        SESSION_USE_SIGNER=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=False,  # Cambiar a True cuando se use HTTPS.
        MAX_CONTENT_LENGTH=2 * 1024 * 1024,
    )
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    server_session.init_app(app)
    csrf.init_app(app)

    from .routes.public import public_bp
    from .routes.admin import admin_bp
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)

    @app.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404

    with app.app_context():
        # Importar modelos antes de create_all para que SQLAlchemy los registre.
        from .models import Usuario, Plato, Pedido, DetallePedido
        db.create_all()
        inicializar_datos()

    return app


def inicializar_datos():
    """Crea administradores y platos de demostración si la BD está vacía."""
    from werkzeug.security import generate_password_hash
    from .models import Usuario, Plato

    administradores = [
        ("Freddy Colina", "12345678*"),
        ("David Reyes", "12345678*"),
    ]
    for username, password in administradores:
        if not Usuario.query.filter_by(username=username).first():
            db.session.add(Usuario(
                username=username,
                password=generate_password_hash(password),
                rol="admin",
            ))

    if Plato.query.count() == 0:
        platos = [
            Plato(nombre="Café americano", descripcion="Café intenso, preparado al momento.", precio=2.50, categoria="Bebidas", imagen_url="https://images.unsplash.com/photo-1511920170033-f8396924c348?w=900"),
            Plato(nombre="Capuchino", descripcion="Espresso con leche vaporizada y espuma cremosa.", precio=3.75, categoria="Bebidas", imagen_url="https://images.unsplash.com/photo-1570968915860-54d5c301fa9f?w=900"),
            Plato(nombre="Té chai", descripcion="Infusión aromática con especias suaves.", precio=3.25, categoria="Bebidas", imagen_url="https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=900"),
            Plato(nombre="Croissant", descripcion="Hojaldre dorado, delicado y recién horneado.", precio=2.80, categoria="Panadería", imagen_url="https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=900"),
            Plato(nombre="Cheesecake", descripcion="Tarta cremosa con base crujiente.", precio=4.50, categoria="Postres", imagen_url="https://images.unsplash.com/photo-1533134242443-d4fd215305ad?w=900"),
            Plato(nombre="Sándwich clásico", descripcion="Pan artesanal, queso, vegetales frescos y salsa de la casa.", precio=5.90, categoria="Comidas", imagen_url="https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=900"),
        ]
        db.session.add_all(platos)

    db.session.commit()
