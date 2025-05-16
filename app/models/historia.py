# models/historia.py

from datetime import datetime
from ..utils.hashing import generar_hash

class HistoriaClinica:
    def __init__(self, paciente_id, contenido):
        self.paciente_id = paciente_id
        self.contenido = contenido
        self.fecha = datetime.now()
        self.hash = generar_hash(contenido)

    def to_tuple(self):
        return (self.paciente_id, self.fecha, self.contenido, self.hash)
