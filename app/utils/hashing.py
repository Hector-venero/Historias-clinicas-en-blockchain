# utils/hashing.py

import hashlib

def generar_hash(contenido):
    return hashlib.sha256(contenido.encode('utf-8')).hexdigest()
