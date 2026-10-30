from functools import wraps
from flask import session, redirect, url_for, flash
from decimal import Decimal, InvalidOperation
from .models import Plato

def admin_requerido(view):
    """Protege una vista: solo permite sesiones autenticadas de administrador."""
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("admin_id"):
            flash("Inicia sesión para acceder al panel administrativo.", "warning")
            return redirect(url_for("admin.login"))
        return view(*args, **kwargs)
    return wrapped

def obtener_carrito():
    """Devuelve el carrito como {id_plato: cantidad}, validando sus datos."""
    carrito = session.get("carrito", {})
    limpio = {}
    for plato_id, cantidad in carrito.items():
        try:
            pid, qty = int(plato_id), int(cantidad)
            if pid > 0 and 1 <= qty <= 99 and Plato.query.filter_by(id=pid, activo=True).first():
                limpio[str(pid)] = qty
        except (TypeError, ValueError):
            continue
    session["carrito"] = limpio
    return limpio

def datos_carrito():
    carrito = obtener_carrito()
    items, total = [], Decimal("0.00")
    for pid, cantidad in carrito.items():
        plato = Plato.query.get(int(pid))
        if plato:
            subtotal = Decimal(str(plato.precio)) * cantidad
            items.append({"plato": plato, "cantidad": cantidad, "subtotal": subtotal})
            total += subtotal
    return items, total

def decimal_seguro(valor):
    try:
        numero = Decimal(str(valor)).quantize(Decimal("0.01"))
        if numero < 0:
            raise InvalidOperation
        return numero
    except (InvalidOperation, ValueError, TypeError):
        return Decimal("0.00")
