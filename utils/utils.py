import hashlib

def validar_integridad(contenido, hash_guardado):
    hash_actual = hashlib.sha256(contenido.encode()).hexdigest()
    return hash_actual == hash_guardado
