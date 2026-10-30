from ..extensions import db

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Hash, nunca texto plano.
    rol = db.Column(db.String(20), nullable=False, default="admin")

    def es_administrador(self):
        return self.rol == "admin"

    def __repr__(self):
        return f"<Usuario {self.username}>"
