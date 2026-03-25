from ecdsa import VerifyingKey, SECP256k1, BadSignatureError
import hashlib

# Fungsi verifikasi tanda tangan mahasiswa
def verify_signature(public_key_hex, signature_hex, nama, keterangan):
    try:
        # Load public key dari format hex
        pub_key = VerifyingKey.from_string(bytes.fromhex(public_key_hex), curve=SECP256k1)
        
        # Gabung data buat dicek integritasnya
        data_string = f"{nama}-{keterangan}"
        message_hash = hashlib.sha256(data_string.encode()).digest()
        
        # Cek cocok atau nggak signature-nya
        signature_bytes = bytes.fromhex(signature_hex)
        return pub_key.verify(signature_bytes, message_hash)
    except (BadSignatureError, ValueError, TypeError):
        # Kalau format salah atau signature gak cocok
        return False
