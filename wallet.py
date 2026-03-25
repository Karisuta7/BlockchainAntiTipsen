from ecdsa import SigningKey, SECP256k1
import hashlib
import json

def generate_data(nama, keterangan):
    # Bikin private dan public key baru
    priv_key = SigningKey.generate(curve=SECP256k1)
    pub_key = priv_key.get_verifying_key()

    # Proses signing data absen
    data = f"{nama}-{keterangan}"
    message = hashlib.sha256(data.encode()).digest()
    signature = priv_key.sign(message).hex()

    return {
        "nama": nama,
        "keterangan": keterangan,
        "public_key": pub_key.to_string().hex(),
        "signature": signature
    }

if __name__ == "__main__":
    payload = generate_data("Tywin Lannister", "Hadir")
    print("--- DATA JSON UNTUK POSTMAN ---")
    print(json.dumps(payload, indent=4))
