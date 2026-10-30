from app import create_app

# Punto de entrada de la aplicación.
app = create_app()

if __name__ == "__main__":
    # debug=True es apropiado únicamente para desarrollo local.
    app.run(host="127.0.0.1", port=5000, debug=True)
