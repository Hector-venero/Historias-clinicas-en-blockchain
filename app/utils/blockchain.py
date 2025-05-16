# utils/web3_utils.py

from web3 import Web3
from app.privada_bfa import PRIVATE_KEY_BFA, ADDRESS_BFA

def publicar_hash_en_bfa(hash_hex):
    web3 = Web3(Web3.HTTPProvider("http://bfa-node:8545"))  # nombre del contenedor en docker-compose

    if not web3.is_connected():
        raise Exception("❌ No se pudo conectar al nodo BFA")

    cuenta = ADDRESS_BFA
    nonce = web3.eth.get_transaction_count(cuenta)

    tx = {
        'nonce': nonce,
        'to': cuenta,  # transacción hacia sí misma
        'value': 0,
        'gas': 21000,
        'gasPrice': web3.to_wei('1', 'gwei'),
        'data': web3.to_bytes(hexstr=hash_hex),
        'chainId': 99118822  # chainId de test2network (BFA test)
    }

    signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY_BFA)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return tx_hash.hex()
