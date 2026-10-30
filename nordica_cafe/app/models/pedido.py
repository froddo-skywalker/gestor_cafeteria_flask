from datetime import datetime
from ..extensions import db

class Pedido(db.Model):
    __tablename__ = "pedidos"

    id = db.Column(db.Integer, primary_key=True)
    cliente_nombre = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(30), nullable=False)
    tipo_servicio = db.Column(db.String(30), nullable=False)  # Tienda Online o Mesa
    mesa_num = db.Column(db.Integer, nullable=True)
    estado = db.Column(db.String(30), nullable=False, default="Pendiente")
    total = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.now)

    detalles = db.relationship(
        "DetallePedido", back_populates="pedido",
        cascade="all, delete-orphan", lazy=True
    )

    def __repr__(self):
        return f"<Pedido #{self.id} - {self.estado}>"
