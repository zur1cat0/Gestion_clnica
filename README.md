# Gestión Clínica de PCs 🖥️💉

Aplicación web en **Django** para gestionar la recepción, diagnóstico, soporte técnico y despacho de equipos de cómputo en una “clínica de PCs”.

Incluye módulos de:
- **Recepción** de equipos
- **Diagnóstico** por parte de estudiantes/técnicos
- **Despacho** y comprobante al cliente

---

## 1. Requisitos previos

Antes de comenzar, asegúrate de tener instalado:

- Git
- Python 3.13 (necesario para instalar todas las dependencias incluidas)
- `pip` (se instala normalmente junto con Python)
- PostgreSQL (requerido por defecto; SQLite está disponible como alternativa)

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

    py -3.13 -m venv clinica_entorno

### Linux / macOS

    python3 -m venv clinica_entorno

Esto creará una carpeta llamada `clinica_entorno` con el entorno aislado de Python.

---

## 4. Activar el entorno virtual (opcional)

### Windows (CMD)

    clinica_entorno\Scripts\activate

### Windows (PowerShell)

    clinica_entorno\Scripts\Activate.ps1

### Linux / macOS

    source clinica_entorno/bin/activate

En Windows también puedes ejecutar los comandos directamente con
`clinica_entorno\Scripts\python.exe`, sin activar el entorno. Si lo activas,
deberías ver algo como:

    (clinica_entorno) C:\ruta\Gestion_clnica>

---

## 5. Instalar las dependencias

Con el entorno virtual **activado**, ejecuta:

    clinica_entorno\Scripts\python.exe -m pip install -r requirements.txt

Esto instalará Django y las demás librerías que el proyecto necesita.

---

## 6. Configurar la base de datos

Por defecto, el proyecto usa PostgreSQL en `localhost:5432` con la base
`clinica_db` y el usuario `postgres`. Copia `.env.example` a `.env` y configura
`DB_PASSWORD` con la contraseña real de PostgreSQL:

### Windows

        copy .env.example .env

### Linux / macOS

        cp .env.example .env

Si tu base o usuario tienen otro nombre, configura también `DB_NAME` o
`DB_USER`. Para seleccionar SQLite explícitamente, establece `DB_ENGINE=sqlite`
en `.env`.

El usuario de PostgreSQL necesita permiso para crear bases de datos. En el
primer inicio, `runserver` crea `DB_NAME` si no existe y aplica las migraciones
automáticamente. También puedes ejecutar `migrate` directamente para preparar
la base antes de iniciar el servidor.

---

## 7. Preparar la base de datos

No necesitas crear la base de datos manualmente. El primer inicio del servidor
la crea si falta y aplica las migraciones. Si quieres prepararla antes:

### Windows

    clinica_entorno\Scripts\python.exe manage.py migrate

### Linux / macOS

    python3 manage.py migrate

Este comando crea la base PostgreSQL si falta y aplica las migraciones.

---

## 8. Crear el superusuario de Django

El servidor debe haberse iniciado al menos una vez para crear la base de datos
y aplicar las migraciones. Este usuario se utilizará para acceder al **admin de
Django**.

### Windows

    clinica_entorno\Scripts\python.exe manage.py createsuperuser

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

    clinica_entorno\Scripts\python.exe manage.py runserver

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
   - **Hardware**
   - **Software**
   - **Despacho**
   - **Salir**

> Nota: El login de la aplicación usa un sistema propio (basado en sesión), diferente del panel `/admin/`.  
> El superusuario de Django se usa para administración interna (crear estudiantes, etc.).

---

### 11.2. Módulo Recepción

- Menú: **Recepción** → “Registrar equipo”

Permite:

- Registrar los datos del cliente (nombre, correo, teléfono).
- Registrar el dispositivo como **PC de escritorio** o **Notebook**.
- Registrar el problema reportado (con opción “Otro” para describirlo) y las
  preguntas realizadas al cliente, con sus respuestas.

Tras guardar, el equipo aparecerá en:

- **Recepción** → “Listado de equipos”
- La información de las preguntas también estará disponible en diagnóstico y
  en los comprobantes e informes de despacho.

Desde el detalle de un equipo se puede:

- Ver toda la información de la recepción.
- Acceder al flujo de diagnóstico.
- Editar o eliminar solo si el equipo **no ha sido despachado** (según las reglas del sistema).

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
- Registrar el diagnóstico inicial y elegir si el equipo sigue a **Hardware**
  o **Software**.
- Si el diagnóstico concluye que ya está listo, marcar **“Listo para despacho”**
  para omitir ambas etapas.
- Guardar.

El sistema:

- Crea el diagnóstico.
- Envía el equipo al área elegida o lo deja listo para despacho cuando se usa
  el bypass.
- Desactiva la asignación del diagnóstico inicial.

#### c) Historial de diagnósticos

- Ir a: **Diagnóstico** → **“Historial completo de diagnósticos”**.
- Desde allí se pueden ver todos los diagnósticos y, según las reglas del sistema:
  - Editar o eliminar diagnósticos **cuando el equipo aún no ha sido despachado al cliente**.

---

### 11.4. Módulo Hardware

- Menú: **Hardware**.
- Registra el diagnóstico físico y la solución aplicada.
- Después de cada intervención se puede enviar el equipo a **Software** o
  dejarlo **listo para despacho**.

### 11.5. Módulo Software

- Menú: **Software**.
- Registra el diagnóstico de software y la solución aplicada.
- Después de cada intervención se puede enviar el equipo a **Hardware** o
  dejarlo **listo para despacho**.
- El historial conserva cada intervención, por lo que un equipo puede pasar
  de un área a la otra según lo que se encuentre.

### 11.6. Módulo Despacho

En la barra de navegación, entra a **Despacho**. Solo aparecen equipos
marcados como listos después del diagnóstico, Hardware o Software.

#### a) Registrar un nuevo despacho

- Ir a: **Despacho** → “Registrar nuevo despacho”.
- Seleccionar un equipo listo para despacho.
- Ingresar:
  - Observaciones (opcional).
- Guardar.

Se genera el comprobante de despacho con el diagnóstico inicial y todas las
intervenciones y soluciones de Hardware y Software.

#### b) Ver listado de despachos

- Ir a: **Despacho** → “Listado de despachos”.
- Desde allí se puede:
  - Ver el estado de cada despacho (Pendiente / Despachado).
  - Acceder al **comprobante de despacho**.
  - Confirmar el despacho al cliente (cuando aún está pendiente).
  - Eliminar o editar despachos, con las restricciones correspondientes.

#### c) Confirmar despacho

- Desde el listado o el comprobante, pulsar **“Confirmar despacho”**.
- El sistema:
  - Marca el despacho como completado.
  - Cambia el estado del equipo a **“Despachado”**.

---

## 12. Detener el servidor y desactivar el entorno virtual

Cuando termines de trabajar:

1. En la terminal donde corre el servidor, presiona:

       Ctrl + C

2. Para desactivar el entorno virtual:

       deactivate

---