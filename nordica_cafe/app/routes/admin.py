from decimal import Decimal
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from ..extensions import db
from ..models import Usuario, Plato, Pedido, DetallePedido
from ..utils import admin_requerido

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("admin_id"):
        return redirect(url_for("admin.dashboard"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        usuario = Usuario.query.filter_by(username=username, rol="admin").first()
        if usuario and check_password_hash(usuario.password, password):
            session.clear()
            session["admin_id"] = usuario.id
            session["admin_username"] = usuario.username
            flash(f"Bienvenido, {usuario.username}.", "success")
            return redirect(url_for("admin.dashboard"))
        flash("Usuario o contraseña incorrectos.", "danger")
    return render_template("admin/login.html")

@admin_bp.post("/logout")
@admin_requerido
def logout():
    session.clear()
    flash("La sesión se cerró correctamente.", "info")
    return redirect(url_for("admin.login"))

@admin_bp.route("/dashboard")
@admin_requerido
def dashboard():
    pedidos = Pedido.query.order_by(Pedido.fecha.desc()).limit(100).all()
    pendientes = Pedido.query.filter_by(estado="Pendiente").count()
    entregados = Pedido.query.filter_by(estado="Entregado").count()
    return render_template(
        "admin/dashboard.html", pedidos=pedidos,
        pendientes=pendientes, entregados=entregados
    )

@admin_bp.post("/pedido/<int:pedido_id>/estado")
@admin_requerido
def cambiar_estado(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    estado = request.form.get("estado")
    if estado in ("Pendiente", "Entregado"):
        pedido.estado = estado
        db.session.commit()
        flash(f"Pedido #{pedido.id}: estado actualizado.", "success")
    else:
        flash("Estado no válido.", "danger")
    return redirect(url_for("admin.dashboard"))

@admin_bp.route("/nuevo-pedido-salon", methods=["GET", "POST"])
@admin_requerido
def nuevo_pedido_salon():
    platos = Plato.query.filter_by(activo=True).order_by(Plato.nombre).all()
    if request.method == "POST":
        nombre = request.form.get("cliente_nombre", "").strip()
        telefono = request.form.get("telefono", "").strip()
        try:
            mesa = int(request.form.get("mesa_num", ""))
            if mesa < 1:
                raise ValueError
        except ValueError:
            mesa = None

        seleccion = []
        total = Decimal("0.00")
        for plato in platos:
            try:
                cantidad = int(request.form.get(f"cantidad_{plato.id}", 0))
            except (ValueError, TypeError):
                cantidad = 0
            if 1 <= cantidad <= 99:
                subtotal = Decimal(str(plato.precio)) * cantidad
                seleccion.append((plato, cantidad, subtotal))
                total += subtotal

        if len(nombre) < 2 or len(nombre) > 120 or not telefono or len(telefono) > 30:
            flash("Completa un nombre y teléfono válidos.", "danger")
        elif not mesa:
            flash("Indica un número de mesa válido.", "danger")
        elif not seleccion:
            flash("Selecciona al menos un producto.", "warning")
        else:
            pedido = Pedido(
                cliente_nombre=nombre, telefono=telefono,
                tipo_servicio="Mesa", mesa_num=mesa,
                estado="Pendiente", total=total
            )
            for plato, cantidad, subtotal in seleccion:
                pedido.detalles.append(DetallePedido(
                    plato_id=plato.id, cantidad=cantidad, subtotal=subtotal
                ))
            db.session.add(pedido)
            db.session.commit()
            flash(f"Pedido de salón #{pedido.id} registrado.", "success")
            return redirect(url_for("admin.dashboard"))

    return render_template("admin/nuevo_pedido.html", platos=platos)
