# Gestión Clínica de PCs 🖥️💉

Aplicación web en **Django** para gestionar la recepción, diagnóstico y entrega de equipos de cómputo en una “clínica de PCs”.

Incluye módulos de:
- **Recepción** de equipos
- **Diagnóstico** por parte de estudiantes/técnicos
- **Entrega** y comprobante al cliente

---

## 1. Requisitos previos

Antes de comenzar, asegúrate de tener instalado:

- Git
- Python 3.x (recomendado 3.11+)
- `pip` (se instala normalmente junto con Python)

Opcional pero recomendado:
- Un editor de código (VS Code, PyCharm, etc.)

---

## 2. Clonar el repositorio

En una terminal o consola:

    git clone https://github.com/zur1cat0/Gestion_clnica.git
    cd Gestion_clnica

A partir de aquí, **todos los comandos** se ejecutan dentro de la carpeta `Gestion_clnica` (donde está `manage.py`).

---

## 3. Crear el entorno virtual `clinica_entorno`

### Windows

En la terminal (CMD o PowerShell), dentro de la carpeta del proyecto:

    python -m venv clinica_entorno

### Linux / macOS

    python3 -m venv clinica_entorno

Esto creará una carpeta llamada `clinica_entorno` con el entorno aislado de Python.

---

## 4. Activar el entorno virtual

### Windows (CMD)

    clinica_entorno\Scripts\activate

### Windows (PowerShell)

    clinica_entorno\Scripts\Activate.ps1

### Linux / macOS

    source clinica_entorno/bin/activate

Si todo está bien, en la consola deberías ver algo como:

    (clinica_entorno) C:\ruta\Gestion_clnica>

---

## 5. Instalar las dependencias

Con el entorno virtual **activado**, ejecuta:

    pip install -r requirements.txt

Esto instalará Django y las demás librerías que el proyecto necesita.

---

## 6. Configurar el archivo `.env`

En el repositorio puede venir un archivo de ejemplo, por ejemplo: `.env.example`.

1. Copia ese archivo a `.env`:

   ### Windows

        copy .env.example .env

   ### Linux / macOS

        cp .env.example .env

2. Si lo deseas, puedes abrir `.env` en tu editor y ajustar valores como:
   - `DEBUG`
   - `SECRET_KEY`
   - Otros parámetros de configuración

Para un entorno local de pruebas normalmente basta con dejar los valores por defecto.

---

## 7. Aplicar migraciones de la base de datos

Con el entorno virtual activado y estando en la carpeta del proyecto:

### Windows

    python manage.py migrate

### Linux / macOS

    python3 manage.py migrate

Esto creará/actualizará las tablas necesarias en la base de datos (por defecto, SQLite).

---

## 8. Crear el superusuario de Django

Este usuario se utilizará para acceder al **admin de Django**.

### Windows

    python manage.py createsuperuser

### Linux / macOS

    python3 manage.py createsuperuser

La consola te pedirá:

- Nombre de usuario
- Correo electrónico (puede ser ficticio)
- Contraseña (se escribirá sin mostrarse en pantalla)

---

## 9. Ejecutar el servidor de desarrollo

Con el entorno activado:

### Windows

    python manage.py runserver

### Linux / macOS

    python3 manage.py runserver

Por defecto se levantará en:

    http://127.0.0.1:8000/

Abre ese enlace en tu navegador.

Para detener el servidor, vuelve a la consola y presiona:

    Ctrl + C

---

## 10. Ingresar al administrador de Django y crear estudiantes

Los estudiantes (técnicos) que participan en el diagnóstico se administran desde el **admin de Django**.

1. Con el servidor corriendo, abre en el navegador:

       http://127.0.0.1:8000/admin/

2. Inicia sesión con el superusuario que creaste en el paso 8.

3. Dentro de la interfaz de administración:
   - Busca la sección correspondiente a la app **Diagnóstico** (o similar).
   - Haz clic en **Estudiantes**.
   - Pulsa en **“Add”** o **“Agregar estudiante”**.
   - Completa los campos requeridos (nombre, correo, teléfono si aplica).
   - Guarda los cambios.
   - Repite para todos los estudiantes/técnicos que quieras registrar.

Estos estudiantes aparecerán luego en los formularios de **asignación de equipo** en el módulo de Diagnóstico.

---

## 11. Uso básico de la aplicación

Una vez que el servidor está en marcha (`runserver`):

### 11.1. Iniciar sesión en la aplicación

1. En el navegador, ve a:

       http://127.0.0.1:8000/

2. En la barra de navegación superior, haz clic en **“Iniciar sesión”**.
3. Ingresa las credenciales configuradas para el sistema de login (según el flujo definido en la app).
4. Al autenticarse correctamente, el menú mostrará las secciones:
   - **Recepción**
   - **Diagnóstico**
   - **Entrega**
   - **Salir**

> Nota: El login de la aplicación usa un sistema propio (basado en sesión), diferente del panel `/admin/`.  
> El superusuario de Django se usa para administración interna (crear estudiantes, etc.).

---

### 11.2. Módulo Recepción

- Menú: **Recepción** → “Registrar equipo”

Permite:

- Registrar los datos del cliente (nombre, correo, teléfono).
- Registrar los datos del equipo (tipo, problema reportado, opción “Otro” con campo libre).

Tras guardar, el equipo aparecerá en:

- **Recepción** → “Listado de equipos”

Desde el detalle de un equipo se puede:

- Ver toda la información de la recepción.
- Acceder al flujo de diagnóstico.
- Editar o eliminar solo si el equipo **no ha sido entregado** (según las reglas del sistema).

---

### 11.3. Módulo Diagnóstico

En la barra de navegación, entra a **Diagnóstico**.

#### a) Asignar equipo a estudiante

- Ir a: **Diagnóstico** → “Asignar equipo”
- Elegir:
  - Estudiante/técnico (desde los creados en el admin).
  - Equipo recepcionado pendiente.
- Guardar la asignación.

El equipo pasará a estado **“En diagnóstico”**.

#### b) Evaluar equipo

- Ir a: **Diagnóstico** → “Evaluar equipo”
- Seleccionar la asignación (estudiante + equipo).
- Completar:
  - Diagnóstico.
  - Tipo de solución (Preventiva / Correctiva).
  - Detalle de la solución aplicada.
- Guardar.

El sistema:

- Crea el diagnóstico.
- Marca el equipo como **“Listo para entrega”**.
- Desactiva la asignación.

#### c) Historial de diagnósticos

- Ir a: **Diagnóstico** → **“Historial completo de diagnósticos”**.
- Desde allí se pueden ver todos los diagnósticos y, según las reglas del sistema:
  - Editar o eliminar diagnósticos **cuando el equipo aún no ha sido entregado al cliente**.

---

### 11.4. Módulo Entrega

En la barra de navegación, entra a **Entrega**.

#### a) Registrar una nueva entrega

- Ir a: **Entrega** → “Registrar nueva entrega”.
- Seleccionar un diagnóstico pendiente de entrega.
- Ingresar:
  - Monto a cobrar.
  - Observaciones (opcional).
- Guardar.

Se genera un registro de entrega asociado al diagnóstico.

#### b) Ver listado de entregas

- Ir a: **Entrega** → “Listado de entregas”.
- Desde allí se puede:
  - Ver el estado de cada entrega (Pendiente / Entregado).
  - Acceder al **comprobante de entrega**.
  - Confirmar la entrega al cliente (cuando aún está pendiente).
  - Eliminar o editar entregas, con las restricciones correspondientes.

#### c) Confirmar entrega

- Desde el listado o el comprobante, pulsar **“Marcar como entregado / Confirmar entrega”**.
- El sistema:
  - Marca la entrega como completada.
  - Cambia el estado del equipo a **“Entregado”**.

---

## 12. Detener el servidor y desactivar el entorno virtual

Cuando termines de trabajar:

1. En la terminal donde corre el servidor, presiona:

       Ctrl + C

2. Para desactivar el entorno virtual:

       deactivate

---