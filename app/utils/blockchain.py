from web3 import Web3
from app.privada_bfa import PRIVATE_KEY_BFA, ADDRESS_BFA
from web3.middleware import geth_poa_middleware

def publicar_hash_en_bfa(hash_hex):
    provider_url = "http://bfa-node:8545"
    web3 = Web3(Web3.HTTPProvider(provider_url))

    # Middleware necesario para redes tipo Proof of Authority (como Clique)
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    if not web3.is_connected():
        raise ConnectionError("❌ No se pudo conectar al nodo BFA")

    cuenta = Web3.to_checksum_address(ADDRESS_BFA)
    print(f"📍 Usando cuenta: {cuenta}")

    balance = web3.eth.get_balance(cuenta)
    print(f"💰 Balance actual: {web3.from_wei(balance, 'ether')} ETH")

    if balance == 0:
        raise ValueError("❌ La cuenta no tiene fondos.")

    nonce = web3.eth.get_transaction_count(cuenta)
    print(f"🔢 Nonce: {nonce}")

    gas_price = web3.to_wei(4, 'gwei')  # Gas price fijo para pruebas
    print(f"⛽ Enviando transacción legacy con gasPrice: {gas_price} wei")

    # Construcción inicial de la transacción sin el campo `gas`
    tx = {
        'nonce': nonce,
        'to': "0x000000000000000000000000000000000000dEaD",
        'value': 0,
        'data': web3.to_bytes(hexstr=hash_hex),
        'gasPrice': gas_price,
        'chainId': 99118822,
        'from': cuenta  
    }

    try:
        estimated_gas = web3.eth.estimate_gas(tx)
        print(f"⛽ Gas estimado: {estimated_gas}")
        tx['gas'] = estimated_gas
        del tx['from']  # 👈 Importante: eliminar `from` antes de firmar
    except Exception as e:
        raise RuntimeError(f"❌ No se pudo estimar el gas: {str(e)}")

    # Firma y envío
    signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY_BFA)
    print("📝 Transacción firmada, enviando...")

    try:
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"✅ Hash publicado con éxito: {tx_hash.hex()}")
        return tx_hash.hex()
    except Exception as e:
        raise RuntimeError(f"❌ Error al enviar la transacción: {str(e)}")
