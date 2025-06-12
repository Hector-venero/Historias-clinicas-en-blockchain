from flask import render_template, request, redirect, url_for, flash, send_file
from datetime import datetime
from . import app
from .database import get_connection
from .auth import Usuario
from .utils.hashing import generar_hash
from .utils.utils import validar_integridad
from .utils.blockchain import publicar_hash_en_bfa
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Usuario.obtener_por_username(username)

        if user and user.verificar_password(password):
            login_user(user)
            return redirect(url_for('index'))
        return render_template('login.html', error='Credenciales incorrectas')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrar')
@login_required
def registrar():
    return render_template('registrar.html')

@app.route('/buscar')
@login_required
def buscar_form():
    return render_template('buscar.html')

@app.route('/resultados')
def resultados():
    filtro = request.args.get('filtro')
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT h.id, h.fecha, h.hash, p.id as paciente_id, p.nombre, p.dni
    FROM historias h
    JOIN pacientes p ON h.paciente_id = p.id
    WHERE p.dni = %s OR UPPER(p.nombre) LIKE UPPER(%s) OR UPPER(p.apellido) LIKE UPPER(%s)
    """, (filtro, f"%{filtro}%", f"%{filtro}%"))

    resultados = cursor.fetchall()
    conn.close()

    return render_template('resultados.html', resultados=resultados, filtro=filtro)

@app.route('/crear_usuario', methods=['GET', 'POST'])
@login_required
def crear_usuario():
    mensaje = None
    error = None

    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        username = request.form['username'].strip()
        password = request.form['password']

        # Validar campos vacíos
        if not nombre or not username or not password:
            error = "Todos los campos son obligatorios."
        elif len(password) < 4:
            error = "La contraseña debe tener al menos 4 caracteres."
        else:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id FROM usuarios WHERE username = %s", (username,))
            existente = cursor.fetchone()

            if existente:
                error = f"El nombre de usuario '{username}' ya existe."
            else:
                password_hash = generate_password_hash(password)
                cursor.execute("""
                    INSERT INTO usuarios (nombre, username, password_hash)
                    VALUES (%s, %s, %s)
                """, (nombre, username, password_hash))
                conn.commit()
                mensaje = f"✅ Usuario '{username}' creado con éxito."

            cursor.close()
            conn.close()

    return render_template('crear_usuario.html', mensaje=mensaje, error=error)


@app.route('/paciente/<int:paciente_id>')
@login_required
def ver_paciente(paciente_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM pacientes WHERE id = %s", (paciente_id,))
    paciente = cursor.fetchone()

    cursor.execute("""
        SELECT * FROM historias
        WHERE paciente_id = %s
        ORDER BY fecha DESC
    """, (paciente_id,))
    historias = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('paciente.html', paciente=paciente, historias=historias)

@app.route('/guardar', methods=['POST'])
@login_required
def guardar():
    print("📍 Entrando a guardar()")
    dni = request.form['dni']
    apellido = request.form['apellido'].upper()
    nombre = request.form['nombre'].upper()
    fecha_nacimiento = request.form.get('fecha_nacimiento')
    sexo = request.form.get('sexo')

    motivo_consulta = request.form.get('motivo_consulta', '').strip()
    antecedentes = request.form.get('antecedentes', '').strip()
    examen_fisico = request.form.get('examen_fisico', '').strip()
    diagnostico = request.form.get('diagnostico', '').strip()
    tratamiento = request.form.get('tratamiento', '').strip()
    observaciones = request.form.get('observaciones', '').strip()
    fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    hash_contenido = generar_hash(
        motivo_consulta + antecedentes + examen_fisico + diagnostico + tratamiento + observaciones
    )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM pacientes WHERE dni = %s", (dni,))
    paciente = cursor.fetchone()

    if paciente:
        paciente_id = paciente[0]
    else:
        cursor.execute("""
            INSERT INTO pacientes (dni, apellido, nombre, fecha_nacimiento, sexo)
            VALUES (%s, %s, %s, %s, %s)
        """, (dni, apellido, nombre, fecha_nacimiento, sexo))
        paciente_id = cursor.lastrowid

    try:
        tx_hash = publicar_hash_en_bfa(hash_contenido)
        if not tx_hash:
            raise ValueError("La transacción no devolvió un hash válido.")
        flash("✅ Historia registrada y hash publicada en la blockchain.", "success")
    except Exception as e:
        tx_hash = None
        flash("⚠️ Historia registrada pero hubo un error al publicar en la blockchain.", "warning")
        print("❌ Error al publicar hash en BFA:", str(e))

    cursor.execute("""
        INSERT INTO historias (paciente_id, usuario_id, fecha, motivo_consulta, antecedentes, examen_fisico, diagnostico, tratamiento, observaciones, hash, tx_hash)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (paciente_id, current_user.id, fecha, motivo_consulta, antecedentes, examen_fisico, diagnostico, tratamiento, observaciones, hash_contenido, tx_hash))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('index'))

@app.route('/historia/<int:id>')
def mostrar_historia(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM historias WHERE id = %s", (id,))
    historia = cursor.fetchone()

    if not historia:
        return "Historia no encontrada", 404

    cursor.execute("SELECT * FROM pacientes WHERE id = %s", (historia['paciente_id'],))
    paciente = cursor.fetchone()

    conn.close()

    historia['valida'] = validar_integridad(
        f"{historia['motivo_consulta']}{historia['antecedentes']}{historia['examen_fisico']}{historia['diagnostico']}{historia['tratamiento']}{historia['observaciones']}",
        historia['hash']
    )

    return render_template("historia.html", historia=historia, paciente=paciente, es_valida=historia['valida'])


@app.route('/historias/<dni>')
@login_required
def historias_paciente(dni):
    desde = request.args.get('desde')
    hasta = request.args.get('hasta')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM pacientes WHERE dni = %s", (dni,))
    paciente = cursor.fetchone()
    if not paciente:
        return "Paciente no encontrado", 404

    query = "SELECT * FROM historias WHERE paciente_id = %s"
    params = [paciente['id']]

    if desde:
        query += " AND fecha >= %s"
        params.append(desde)
    if hasta:
        query += " AND fecha <= %s"
        params.append(hasta)

    query += " ORDER BY fecha DESC"

    cursor.execute(query, tuple(params))
    historias = cursor.fetchall()
    cursor.close()
    conn.close()

    for h in historias:
        contenido_concat = f"{h['motivo_consulta']}{h['antecedentes']}{h['examen_fisico']}{h['diagnostico']}{h['tratamiento']}{h['observaciones']}"
        h['valida'] = validar_integridad(contenido_concat, h['hash'])

    return render_template("historias_paciente.html", paciente=paciente, historias=historias, desde=desde, hasta=hasta)


@app.route('/exportar_pdf/<int:id>')
@login_required
def exportar_pdf(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM historias WHERE id = %s", (id,))
    historia = cursor.fetchone()

    if not historia:
        return "Historia no encontrada", 404

    cursor.execute("SELECT * FROM pacientes WHERE id = %s", (historia['paciente_id'],))
    paciente = cursor.fetchone()

    conn.close()

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, 750, f"Historia Clínica de {paciente['apellido']}, {paciente['nombre']} (DNI: {paciente['dni']})")

    p.setFont("Helvetica", 12)
    y = 720
    p.drawString(50, y, f"Fecha: {historia['fecha']}")
    y -= 20

    campos = [
        ("Motivo de Consulta", historia['motivo_consulta']),
        ("Antecedentes", historia['antecedentes']),
        ("Examen Físico", historia['examen_fisico']),
        ("Diagnóstico", historia['diagnostico']),
        ("Tratamiento", historia['tratamiento']),
        ("Observaciones", historia['observaciones'])
    ]

    for titulo, contenido in campos:
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y, titulo + ":")
        y -= 15
        p.setFont("Helvetica", 11)
        for linea in contenido.splitlines():
            p.drawString(60, y, linea[:100])  # limitar línea larga
            y -= 15
        y -= 10

    p.drawString(50, y, f"Hash: {historia['hash']}")
    p.showPage()
    p.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='historia_clinica.pdf', mimetype='application/pdf')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
