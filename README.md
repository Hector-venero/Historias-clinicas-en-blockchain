# 🏥 Historias Clínicas en Blockchain - UNSAM CAU

Este proyecto implementa un sistema web de gestión de historias clínicas, desarrollado como trabajo final integrador de la carrera de Ingeniería en Telecomunicaciones de la Universidad Nacional de San Martín (UNSAM). El sistema garantiza la integridad y trazabilidad de los datos mediante el uso combinado de una base de datos relacional y la Blockchain Federal Argentina (BFA).

---

## 📌 Funcionalidades Principales

- Registro, consulta y exportación en PDF de historias clínicas.
- Hash SHA-256 para garantizar la integridad de cada historia.
- Publicación opcional del hash en la BFA usando Web3.
- Seguridad mediante login con Flask-Login y contraseñas encriptadas.
- Validación de integridad de registros clínicos.
- Interfaz web simple, accesible desde navegadores internos del CAU.

---

## 🧱 Tecnologías Utilizadas

- **Backend:** Python (Flask)
- **Base de datos:** MySQL 8.0
- **Blockchain:** Nodo Geth configurado con test2network (BFA)
- **Contenedores:** Docker + Docker Compose
- **PDF y visualización:** ReportLab + Jinja2

---

## 🐳 Instalación con Docker Compose

1. **Clonar el repositorio**

   ```bash
   git clone https://github.com/Hector-venero/Historias-clinicas-en-blockchain.git
   cd Historias-clinicas-en-blockchain
   ```

2. **Levantar entorno con Docker Compose**

   ```bash
   sudo docker-compose up --build
   ```

   Esto iniciará:

   - `historia_web`: aplicación Flask
   - `historia_db`: base de datos MySQL con init.sql
   - *(Por fuera del Compose)* el nodo `bfa-node` debe levantarse con el script adicional.

3. **Inicializar nodo BFA** (por separado):

   ```bash
   ./reset_bfa_node.sh
   ```

   *(Ver `setup_bfa_node.sh` y `reset_bfa_node.sh` para detalles)*

---

## ▶️ Acceso a la App

Una vez desplegado, accedé desde tu navegador en:

📍 [http://localhost:5000](http://localhost:5000)

Usuario por defecto:
- **Usuario:** `hector`
- **Contraseña:** `2908`

---

## 🗂️ Nueva Estructura del Proyecto

```
.
├── app/
│   ├── __init__.py            # Inicializa Flask y login
│   ├── main.py                # Entrada principal
│   ├── auth.py                # Manejo de usuarios y login
│   ├── routes.py              # Rutas web
│   ├── config.py              # Configuración base de datos
│   ├── database.py            # Conexión MySQL
│   ├── privada_bfa.py         # Claves de la BFA via variables de entorno
│   ├── templates/             # Archivos HTML
│   ├── static/                # Imágenes y estilos
│   ├── models/                # (Opcional) Clases auxiliares
│   └── utils/
│       ├── hashing.py         # SHA-256 y validación
│       ├── blockchain.py      # Publicar en BFA
│       └── utils.py           # Validadores generales
│
├── db/
│   ├── init.sql               # Estructura de la BD + usuario por defecto
│
├── bfa-node/
│   ├── nucleo/                # Nodo Geth con test2network
│   ├── container/             # Dockerfile del nodo
│
├── docker-compose.yml
├── setup_bfa_node.sh
├── reset.sh
├── README.md
```

---

## 🔐 Seguridad y Validación

- Contraseñas encriptadas con `werkzeug.security`.
- Control de acceso con `@login_required`.
- Validación de integridad de historias clínicas al visualizar.
- Registros clínicos inmutables una vez almacenados.
- Almacenamiento off-chain con hash on-chain.

---

## 📦 Scripts Útiles

- `setup_bfa_node.sh`: instala dependencias en el contenedor Ubuntu y lanza Geth.
- `reset.sh`: resetea completamente el entorno Docker local (construcción limpia).
- `reset_bfa_node.sh`: reinicia el nodo BFA con mount persistente.

---

## 🖼️ Documentación Adicional

En la carpeta `/docs` se encuentran:

- Diagramas de arquitectura del sistema.
- Diagrama entidad-relación.
- Descripción del modelo de bloques y mecanismos de consenso (PoW vs PoA).
- Capturas de la interfaz web.
- Análisis de seguridad.

---

## 🪪 Licencia

Este proyecto fue desarrollado con fines académicos en el marco del Proyecto Final Integrador de la carrera de Ingeniería en Telecomunicaciones (UNSAM). Su uso está restringido a propósitos educativos o internos institucionales.

---

## 📬 Contacto

**Autor:** Héctor Venero  
**Carrera:** Ingeniería en Telecomunicaciones  
**Universidad:** UNSAM (ECyT)  
**Año:** 2025