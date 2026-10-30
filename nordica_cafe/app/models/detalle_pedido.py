from ..extensions import db

class DetallePedido(db.Model):
    __tablename__ = "detalles_pedido"

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedidos.id"), nullable=False)
    plato_id = db.Column(db.Integer, db.ForeignKey("platos.id"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)

    pedido = db.relationship("Pedido", back_populates="detalles")
    plato = db.relationship("Plato")

    def __repr__(self):
        return f"<DetallePedido {self.cantidad} x plato {self.plato_id}>"
