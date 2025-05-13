# 🏥 Historias Clínicas en Blockchain - UNSAM CAU

Este proyecto implementa un sistema web de gestión de historias clínicas, desarrollado como trabajo final integrador de la carrera de Ingeniería en Telecomunicaciones de la Universidad Nacional de San Martín (UNSAM). El objetivo principal es unificar y asegurar la información clínica mediante el uso de una base de datos relacional y tecnología blockchain (BFA).

---

## 📌 Descripción del Proyecto

- Registro y consulta de historias clínicas con hash de integridad.
- Seguridad mediante login, encriptación y control de sesiones.
- Sistema web accesible desde navegador, pensado para uso interno en el CAU.
- Infraestructura preparada para integrarse con la Blockchain Federal Argentina (BFA).
- Posibilidad de extensión para archivos adjuntos, derivaciones y permisos por rol.

---

## 🧰 Requisitos

- Python 3.10 o superior
- MySQL Server (o MariaDB)
- pip (gestor de paquetes Python)
- (Opcional) Entorno virtual

---

## ⚙️ Instalación

1. **Clonar el repositorio:**

   ```bash
   git clone git@github.com:Hector-venero/Historias-clinicas-en-blockchain.git
   cd Historias-clinicas-en-blockchain
   ```

2. **Crear entorno virtual (recomendado):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar base de datos:**

   - Crear la base de datos desde el archivo `crear_tablas.sql`:

     ```bash
     mysql -u flaskuser -p < crear_tablas.sql
     ```

   - Verificar que el archivo `config.py` contiene los datos correctos de conexión:

     ```python
     DB_CONFIG = {
         'host': 'localhost',
         'user': 'flaskuser',
         'password': 'flaskpass',
         'database': 'hc_bfa'
     }
     ```

---

## ▶️ Ejecución

Con el entorno virtual activado, ejecutá:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Luego accedé en el navegador a: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🗂️ Estructura del Proyecto

```
.
├── app.py               # App principal Flask
├── auth.py              # Lógica de login y seguridad
├── config.py            # Configuración DB
├── crear_tablas.sql     # Script para crear las tablas
├── database.py          # Conexión a base de datos
├── models/              # (Opcional) lógica extendida
├── static/              # Archivos estáticos (img, CSS)
├── templates/           # Vistas HTML
├── utils/               # Hashing y validación
├── requirements.txt     # Dependencias Python
└── README.md            # Este archivo
```

---

## 🔐 Seguridad

- Login con Flask-Login
- Contraseñas encriptadas con `werkzeug.security`
- Control de acceso con decoradores `@login_required`
- Separación de datos: datos personales en base local, hashes en blockchain
- Validación de integridad de historias clínicas mediante regeneración de hash

---

## 🖼️ Capturas y Diagramas

En la carpeta `/docs` se incluyen:

- Diagrama de arquitectura
- Diagrama de autenticación
- Modelo entidad-relación
- Validaciones de seguridad
- Flujo de búsqueda y verificación de integridad

---

## 🪪 Licencia

Este software fue desarrollado con fines académicos en el marco del Proyecto Final Integrador de la carrera de Ingeniería en Telecomunicaciones (UNSAM). Su uso está permitido únicamente con fines educativos, de investigación o internos institucionales.

---

## 📬 Contacto

**Autor:** Héctor Venero  
**Carrera:** Ingeniería en Telecomunicaciones  
**Universidad:** Universidad Nacional de San Martín  
**Año:** 2025  
