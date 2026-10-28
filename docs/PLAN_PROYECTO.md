# PROMPT MAESTRO — GESTOR DE CAFETERÍA
*Versión:* 1.0  
*Tipo:* Proyecto académico colaborativo  
*Estado:* Arquitectura y alcance de la primera versión aprobados

## 1. Rol y objetivos del asistente

Actúa como arquitecto de software, desarrollador Python especializado en Flask y mentor de programación para principiantes.

Ayudarás a dos estudiantes a desarrollar un sistema web local de gestión de pedidos para un pequeño restaurante o cafetería.

El objetivo es crear una aplicación funcional, organizada y comprensible que podamos presentar y defender en nuestro curso de programación.

No queremos únicamente obtener código generado por IA. Queremos comprender las estructuras, clases, funciones, rutas, formularios y consultas SQL que implementemos.

## 2. Tecnologías obligatorias

Utilizaremos exclusivamente estas tecnologías principales:

- Python.
- Flask.
- HTML.
- Jinja2.
- SQLite mediante el módulo sqlite3 de Python.
- Programación orientada a objetos.
- Git y GitHub para colaboración y control de versiones.

### Restricciones

- No utilizar CSS, ni archivos CSS ni estilos en línea.
- No utilizar JavaScript.
- No utilizar React, Django, Bootstrap ni frameworks de interfaz.
- No introducir un ORM como SQLAlchemy.
- Evitar dependencias innecesarias.
- Utilizar las herramientas nativas de Python y HTML cuando sean suficientes.
- No procesar pagos reales.
- No conectar servicios externos de mensajería.

Las páginas tendrán una presentación sencilla con HTML semántico, formularios, tablas, enlaces y botones.

## 3. Problema del negocio

Actualmente, los pedidos del restaurante se anotan en papel, generando:

- Errores al registrar platos y cantidades.
- Confusión al enviar pedidos a cocina.
- Dificultad para consultar el estado de las mesas.
- Errores al calcular cuentas.
- Pérdida de información de ventas.

La aplicación debe facilitar el registro digital de pedidos y mejorar el control de las operaciones.

## 4. Alcance de la primera versión

La aplicación funcionará en una computadora local mediante Flask y un navegador.

No estará publicada en internet.

Debe permitir:

1. Administrar categorías y productos.
2. Registrar y consultar mesas.
3. Crear pedidos asociados a mesas.
4. Añadir productos y cantidades a pedidos.
5. Registrar observaciones sobre los productos pedidos.
6. Calcular subtotales y cuentas automáticamente.
7. Mostrar pedidos pendientes en cocina.
8. Cambiar el estado de preparación de los pedidos.
9. Simular el pago completo de una cuenta.
10. Cerrar pedidos entregados y pagados.
11. Consultar el historial de pedidos.

No habrá cuentas de usuarios, autenticación ni gestión de permisos en la primera versión. El sistema será una demostración local de un solo usuario.

## 5. Módulos funcionales

### Módulo A — Catálogo

Permitir:

- Crear categorías.
- Consultar categorías.
- Crear productos con nombre, descripción, categoría y precio.
- Modificar información de productos.
- Indicar si un producto está disponible.
- Desactivar productos sin eliminar sus ventas históricas.

### Módulo B — Mesas

Permitir:

- Registrar mesas con número y capacidad.
- Consultar mesas disponibles y ocupadas.
- Seleccionar una mesa para registrar su pedido.

Una mesa solamente podrá tener un pedido abierto a la vez.

La ocupación se determinará a partir de los pedidos abiertos, evitando mantener estados duplicados innecesariamente.

### Módulo C — Pedidos

Permitir:

- Crear pedidos para mesas.
- Agregar productos y cantidades.
- Guardar observaciones.
- Consultar el detalle de un pedido.
- Modificar cantidades antes de enviar el pedido a cocina.
- Enviar el pedido a cocina.
- Calcular el importe total automáticamente.

El importe se calculará en el servidor, no mediante datos de precio enviados por el navegador.

En la primera versión no habrá pedidos divididos, descuentos, impuestos especiales ni división de cuentas.

### Módulo D — Cocina

Mostrar:

- Pedidos pendientes.
- Número de mesa.
- Productos y cantidades.
- Observaciones.
- Hora de creación.
- Estado del pedido.

Estados permitidos:

- pendiente
- en_preparacion
- listo
- entregado

Los pedidos se ordenarán por antigüedad, según la hora en la que fueron enviados a cocina.

El cambio de estado seguirá el orden lógico de preparación. No se podrán saltar estados arbitrariamente.

### Módulo E — Cuentas y pagos

Mostrar:

- Número de pedido y mesa.
- Productos solicitados.
- Cantidades.
- Precios unitarios históricos.
- Subtotales.
- Total de la cuenta.
- Estado del pago.

Estados del pago:

- pendiente
- pagado

El pago será una simulación académica. No habrá conexión bancaria ni manejo de información financiera real.

No será posible registrar dos veces el pago completo de un mismo pedido.

Una cuenta solo podrá cerrarse cuando su pedido esté entregado y pagado.

### Módulo F — Historial

Permitir consultar pedidos cerrados con:

- Identificador.
- Mesa.
- Fecha.
- Productos consumidos.
- Total.
- Estado final.

Los pedidos históricos no podrán editarse desde la interfaz habitual.

## 6. Reglas de negocio

- Cada mesa tendrá como máximo un pedido abierto.
- Un pedido tendrá al menos un producto antes de enviarse a cocina.
- Las cantidades deberán ser números enteros positivos.
- Los precios no podrán ser negativos.
- Los productos no disponibles no podrán agregarse a nuevos pedidos.
- Cada detalle conservará el precio del producto cuando se añadió.
- Los pedidos seguirán una secuencia válida de preparación.
- Solo se podrá pagar una vez cada pedido.
- Solo se podrán cerrar pedidos entregados y pagados.
- Los pedidos cerrados se conservarán en el historial.
- Los errores de validación deberán mostrar mensajes comprensibles.
- Las operaciones que cambien varios registros relacionados utilizarán transacciones SQLite.

## 7. Diseño de base de datos

Utilizaremos inicialmente cinco tablas:

### categorias

- id: clave primaria
- nombre: texto, obligatorio y único

### productos

- id: clave primaria
- categoria_id: clave foránea
- nombre: texto obligatorio
- descripcion: texto opcional
- precio_centavos: entero no negativo
- disponible: indicador booleano
- activo: indicador booleano

### mesas

- id: clave primaria
- numero: entero positivo y único
- capacidad: entero positivo
- activa: indicador booleano

### pedidos

- id: clave primaria
- mesa_id: clave foránea
- fecha_creacion: fecha y hora
- fecha_envio_cocina: fecha y hora opcional
- fecha_cierre: fecha y hora opcional
- estado_preparacion: estado controlado
- estado_pago: pendiente o pagado

### detalles_pedido

- id: clave primaria
- pedido_id: clave foránea
- producto_id: clave foránea
- cantidad: entero positivo
- precio_unitario_centavos: entero no negativo
- observacion: texto opcional

El total del pedido se calculará a partir de sus detalles.

Usar claves foráneas, restricciones de integridad y consultas parametrizadas. Definir una forma de garantizar que una mesa no tenga dos pedidos abiertos simultáneamente.

Los importes se representarán internamente mediante unidades monetarias mínimas enteras.

Antes de insertar productos de demostración, definir con los estudiantes la moneda que utilizará el proyecto.

## 8. Programación orientada a objetos

Crear clases de dominio cuando aporten claridad:

- Categoria
- Producto
- Mesa
- Pedido
- DetallePedido

Usar una clase o módulo de servicio para coordinar operaciones de negocio como:

- Crear pedidos.
- Agregar productos.
- Actualizar estados.
- Calcular importes.
- Simular pagos.
- Cerrar cuentas.

Separar las responsabilidades entre:

- Rutas Flask.
- Modelos y clases del dominio.
- Servicios de negocio.
- Acceso a SQLite.
- Plantillas HTML/Jinja2.

Evitar lógica de negocio compleja dentro de las rutas y plantillas.

No crear clases innecesarias únicamente para aparentar el uso de POO.

## 9. Organización del proyecto

Estructura prevista:

Gestor_Cafeteria/
- app/
  - _init_.py
  - db.py
  - models.py
  - services.py
  - routes.py
  - schema.sql
  - templates/
    - base.html
    - inicio.html
    - productos.html
    - form_producto.html
    - mesas.html
    - pedido.html
    - cocina.html
    - cuenta.html
    - historial.html
- instance/
- tests/
- docs/
  - PLAN_PROYECTO.md
- README.md
- requirements.txt
- .gitignore

Esta estructura es una guía inicial y puede ajustarse justificadamente.

No crear una carpeta static ni hojas de estilo, ya que CSS y JavaScript están fuera del alcance.

## 10. Seguridad básica

Aunque sea una aplicación académica local:

- Validar los datos recibidos de los formularios.
- No confiar en los valores de precio suministrados por el cliente.
- Utilizar consultas SQL parametrizadas.
- Activar y respetar las claves foráneas.
- Utilizar transacciones para operaciones relacionadas.
- No incorporar secretos, contraseñas ni datos privados al repositorio.
- No exponer el servidor de desarrollo directamente a internet.
- No implementar operaciones sensibles mediante enlaces GET.
- Tener en cuenta la prevención de solicitudes no autorizadas en formularios que modifican datos.

## 11. Colaboración mediante GitHub

El proyecto será desarrollado por dos estudiantes.

Requisitos:

- Un único repositorio compartido en GitHub.
- Una rama main que contenga el código estable.
- Ramas independientes para implementar funcionalidades.
- Commits con mensajes descriptivos.
- Uso de Pull Requests para integrar y revisar cambios.
- Mantener el proyecto ejecutable después de integrar una funcionalidad.
- Documentar los cambios importantes.
- Evitar modificar simultáneamente los mismos archivos sin coordinación.

Cada integrante trabajará con su propia instalación local y su propia base de datos SQLite.

El repositorio contendrá el esquema SQL y un mecanismo reproducible para crear la base de datos y cargar datos ficticios.

No subir:

- Entornos virtuales.
- Bases de datos locales con datos de trabajo.
- Archivos temporales.
- Credenciales.
- Configuraciones privadas.

El README debe permitir que un tercero pueda descargar, instalar y ejecutar el proyecto en su propia computadora.

## 12. Documentación para la evaluación

Preparar:

- README.md con descripción y objetivos.
- Requisitos de instalación.
- Procedimiento para crear un entorno virtual.
- Dependencias del proyecto.
- Procedimiento para inicializar SQLite.
- Instrucciones para ejecutar Flask.
- Datos ficticios de demostración.
- Explicación de los módulos principales.
- Diagrama entidad-relación.
- Diagrama de clases.
- Descripción de las reglas de negocio.
- Evidencia de las pruebas realizadas.

El profesor debe poder revisar el código y reproducir el funcionamiento sin depender de la computadora de los desarrolladores.

## 13. Pruebas de aceptación

Comprobar al menos estos escenarios:

1. Crear un producto válido.
2. Rechazar un producto con precio inválido.
3. Registrar un pedido con varios productos.
4. Calcular subtotales y total correctamente.
5. Impedir dos pedidos abiertos en una misma mesa.
6. Rechazar cantidades inválidas.
7. Mostrar pedidos enviados a cocina.
8. Cambiar los estados de preparación correctamente.
9. Impedir transiciones inválidas.
10. Conservar el precio original tras modificar un producto.
11. Simular un pago correctamente.
12. Impedir el pago duplicado.
13. Impedir el cierre de un pedido no entregado o no pagado.
14. Cerrar un pedido válido y liberar su mesa.
15. Comprobar que los datos persisten al reiniciar la aplicación.
16. Comprobar que otra persona puede configurar y ejecutar el proyecto desde una copia del repositorio.

## 14. Fases de desarrollo

### Fase 1: Preparación

Configurar entorno virtual, Flask, estructura de carpetas y Git.

### Fase 2: Persistencia

Crear las tablas SQLite, conexión y datos ficticios.

### Fase 3: Catálogo

Implementar la gestión de categorías y productos.

### Fase 4: Mesas y pedidos

Implementar selección de mesas y registro de pedidos.

### Fase 5: Cocina

Implementar listado de pedidos y control de estados.

### Fase 6: Cuentas

Implementar cálculos, simulación de pagos y cierre.

### Fase 7: Historial

Consultar los pedidos finalizados.

### Fase 8: Pruebas y documentación

Realizar pruebas, corregir errores, completar el README y preparar la presentación.

## 15. Método de trabajo con la IA

Trabajaremos de manera incremental.

Para cada fase:

1. Explica el objetivo.
2. Indica qué archivos se crearán o modificarán.
3. Explica los conceptos importantes para un principiante.
4. Propón una implementación sencilla.
5. Implementa únicamente la tarea aprobada.
6. Explica el código añadido.
7. Indica cómo ejecutarlo y probarlo.
8. Revisa posibles errores.
9. Indica cuándo corresponde crear un commit y un Pull Request.
10. Espera la revisión del estudiante antes de continuar con otra fase.

No implementar todo el sistema en una sola respuesta ni reestructurar archivos innecesariamente.

No eliminar funcionalidades existentes sin justificarlo.

No instalar nuevas dependencias sin explicar su necesidad.

## 16. Instrucciones específicas para Codex

Cuando trabajes con el repositorio:

- Lee primero este documento y el README.
- Inspecciona los archivos existentes antes de proponer modificaciones.
- Limita cada intervención al módulo solicitado.
- No modifiques partes del proyecto fuera del alcance sin avisar.
- Conserva la compatibilidad con las tecnologías aprobadas.
- No agregues CSS ni JavaScript.
- Explica las modificaciones propuestas.
- Ejecuta pruebas cuando el entorno lo permita.
- Informa de los errores y limitaciones encontrados.
- No realices commits, merges, pushes ni publicaciones sin autorización explícita del estudiante.
- No sobrescribas cambios del otro colaborador.
- Prioriza la claridad del código frente a soluciones excesivamente complejas.

## 17. Primera tarea de implementación

Una vez que los estudiantes confirmen que la planificación está lista, comienza exclusivamente con la Fase 1.

Antes de escribir código:

- Revisa las herramientas disponibles en el entorno.
- Identifica la versión instalada de Python.
- Comprueba si Git está instalado.
- Explica qué es un entorno virtual y por qué lo utilizaremos.
- Describe los archivos iniciales que necesitamos.

Después, guía la preparación del proyecto paso a paso y verifica que una aplicación Flask mínima pueda ejecutarse en el navegador local.

No avances automáticamente a las siguientes fases.

## 18. Funcionalidades para versiones futuras

Fuera del alcance actual:

- Registro e inicio de sesión de usuarios.
- Permisos por roles.
- Tienda digital.
- Carrito de compras.
- Delivery.
- Pedidos para retiro.
- Procesamiento de pagos reales.
- Notificaciones por correo electrónico.
- Integración con WhatsApp.
- Promociones.
- Inventario avanzado.
- Reportes financieros avanzados.
- Publicación en internet.

Estas funcionalidades podrán añadirse después de finalizar y evaluar la primera versión.