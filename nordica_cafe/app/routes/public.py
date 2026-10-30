from decimal import Decimal
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from ..extensions import db
from ..models import Plato, Pedido, DetallePedido
from ..utils import obtener_carrito, datos_carrito

public_bp = Blueprint("public", __name__)

@public_bp.route("/")
def inicio():
    platos = Plato.query.filter_by(activo=True).order_by(Plato.categoria, Plato.nombre).all()
    categorias = sorted({p.categoria for p in platos})
    return render_template("public/index.html", platos=platos, categorias=categorias)

@public_bp.post("/carrito/agregar/<int:plato_id>")
def agregar_carrito(plato_id):
    plato = Plato.query.filter_by(id=plato_id, activo=True).first_or_404()
    carrito = obtener_carrito()
    clave = str(plato.id)
    carrito[clave] = min(carrito.get(clave, 0) + 1, 99)
    session["carrito"] = carrito
    flash(f"{plato.nombre} se agregó al carrito.", "success")
    return redirect(request.referrer or url_for("public.inicio"))

@public_bp.route("/carrito")
def ver_carrito():
    items, total = datos_carrito()
    return render_template("public/carrito.html", items=items, total=total)

@public_bp.post("/carrito/actualizar")
def actualizar_carrito():
    carrito = obtener_carrito()
    nuevo = {}
    for pid in carrito:
        try:
            cantidad = int(request.form.get(f"cantidad_{pid}", 0))
            if 1 <= cantidad <= 99:
                nuevo[pid] = cantidad
        except (ValueError, TypeError):
            pass
    session["carrito"] = nuevo
    flash("Carrito actualizado.", "success")
    return redirect(url_for("public.ver_carrito"))

@public_bp.post("/carrito/eliminar/<int:plato_id>")
def eliminar_carrito(plato_id):
    carrito = obtener_carrito()
    carrito.pop(str(plato_id), None)
    session["carrito"] = carrito
    flash("Producto eliminado del carrito.", "info")
    return redirect(url_for("public.ver_carrito"))

@public_bp.route("/checkout", methods=["GET", "POST"])
def checkout():
    items, total = datos_carrito()
    if not items:
        flash("Tu carrito está vacío. Agrega productos antes de continuar.", "warning")
        return redirect(url_for("public.inicio"))

    if request.method == "POST":
        nombre = request.form.get("cliente_nombre", "").strip()
        telefono = request.form.get("telefono", "").strip()
        if len(nombre) < 2 or len(nombre) > 120 or not telefono or len(telefono) > 30:
            flash("Ingresa un nombre y teléfono válidos.", "danger")
            return render_template("public/checkout.html", items=items, total=total)

        pedido = Pedido(
            cliente_nombre=nombre,
            telefono=telefono,
            tipo_servicio="Tienda Online",
            estado="Pendiente",
            total=total,
        )
        for item in items:
            pedido.detalles.append(DetallePedido(
                plato_id=item["plato"].id,
                cantidad=item["cantidad"],
                subtotal=item["subtotal"],
            ))
        db.session.add(pedido)
        db.session.commit()
        session["carrito"] = {}
        # La factura solo queda accesible desde la sesión que acaba de crearla.
        session["factura_pedido_id"] = pedido.id
        return redirect(url_for("public.factura", pedido_id=pedido.id))

    return render_template("public/checkout.html", items=items, total=total)

@public_bp.route("/factura/<int:pedido_id>")
def factura(pedido_id):
    # Evita que un visitante adivine IDs y consulte datos personales de otros clientes.
    if session.get("factura_pedido_id") != pedido_id:
        from flask import abort
        abort(404)
    pedido = Pedido.query.get_or_404(pedido_id)
    return render_template("public/factura.html", pedido=pedido)
