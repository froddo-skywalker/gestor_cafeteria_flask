from ..extensions import db

class Plato(db.Model):
    __tablename__ = "platos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    categoria = db.Column(db.String(60), nullable=False)
    imagen_url = db.Column(db.String(500), nullable=True)
    activo = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"<Plato {self.nombre}>"
