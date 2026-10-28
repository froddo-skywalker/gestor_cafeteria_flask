# Gestor de Cafetería

Proyecto académico desarrollado en parejas para un curso de programación con Python.

## Descripción

Aplicación web local para gestionar los productos, mesas, pedidos y cuentas de un pequeño restaurante o cafetería.

El objetivo es reducir los errores asociados con las anotaciones manuales, facilitar la comunicación de pedidos a cocina y automatizar el cálculo de las cuentas.

## Tecnologías

- Python
- Flask
- HTML
- Jinja2
- SQLite
- Programación orientada a objetos (POO)
- Git y GitHub

**Restricción académica:** esta primera versión no utiliza CSS ni JavaScript.

## Funcionalidades previstas

- Gestión de categorías y productos.
- Administración de mesas.
- Registro y consulta de pedidos.
- Panel de cocina.
- Seguimiento del estado de los pedidos.
- Cálculo automático de cuentas.
- Simulación de pagos.
- Historial de pedidos.

## Estado del desarrollo

**Fase 1 — Configuración inicial.**

Actualmente contamos con una aplicación mínima de Flask funcionando localmente. Las funcionalidades de gestión del restaurante todavía están pendientes de implementación.

## Requisitos

- Python 3
- Git
- Un navegador web
- Las bibliotecas indicadas en `requirements.txt`

## Instalación en Windows

1. Clonar el repositorio desde GitHub.
2. Abrir la carpeta en Visual Studio Code.
3. Crear un entorno virtual:

   `py -m venv .venv`

4. Instalar las dependencias:

   `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`

5. Ejecutar el servidor Flask:

   `.\.venv\Scripts\python.exe -m flask --app app run`

6. Abrir en el navegador:

   `http://127.0.0.1:5000/`

La aplicación se ejecuta únicamente en la computadora local.

## Base de datos

SQLite será utilizado para almacenar productos, mesas y pedidos.

Su implementación se realizará en una fase posterior. Se proporcionarán instrucciones para inicializarla y generar datos ficticios de prueba.

## Organización del trabajo

El proyecto será desarrollado por dos estudiantes utilizando ramas de Git y Pull Requests para revisar e integrar los cambios.

La rama `main` contendrá las versiones estables.

## Documentación

El análisis, las reglas del negocio, la arquitectura y las fases de desarrollo se encuentran en:

`docs/PLAN_PROYECTO.md`

## Alcance académico

Este sistema se desarrolla con fines educativos. Los pagos serán simulados y no procesará transacciones bancarias reales.
