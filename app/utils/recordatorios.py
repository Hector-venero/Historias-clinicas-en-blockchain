from app.database import get_connection
from flask_mail import Mail, Message
from app import app, mail
from datetime import datetime, timedelta

with app.app_context():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    ahora = datetime.now()
    inicio = ahora + timedelta(hours=24)
    fin = inicio + timedelta(minutes=5)

    cursor.execute("""
        SELECT t.id, t.fecha, p.email, p.nombre, t.motivo
        FROM turnos t
        JOIN pacientes p ON t.paciente_id = p.id
        WHERE t.fecha BETWEEN %s AND %s AND t.notificado = FALSE AND p.email IS NOT NULL
    """, (inicio.strftime('%Y-%m-%d %H:%M:%S'), fin.strftime('%Y-%m-%d %H:%M:%S')))

    turnos = cursor.fetchall()

    for t in turnos:
        msg = Message("Recordatorio de turno",
                      recipients=[t['email']])
        msg.body = f"Hola {t['nombre']}, le recordamos su turno el {t['fecha']}.\nMotivo: {t['motivo'] or 'Consulta médica'}"
        mail.send(msg)
        cursor.execute("UPDATE turnos SET notificado = TRUE WHERE id = %s", (t['id'],))

    conn.commit()
    cursor.close()
    conn.close()
