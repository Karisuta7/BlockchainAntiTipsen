import sys
import json
import os
from flask import Flask, jsonify, request
from blockchain import Blockchain
from signature import verify_signature 

app = Flask(__name__)
blockchain = Blockchain()

# ID unik miner berdasarkan Port agar tidak tertukar
port_id = sys.argv[1] if len(sys.argv) > 1 else "5000"
MINER_ID = f"Admin_Node_{port_id}"
BLOCKCHAIN_FILE = f"blockchain_data_{port_id}.json"
STUDENT_DB_FILE = "students.json"

# --- FUNGSI HELPER PENYIMPANAN ---

def save_chain():
    """Simpan blockchain ke file JSON agar tidak hilang saat server mati"""
    with open(BLOCKCHAIN_FILE, 'w') as f:
        json.dump(blockchain.chain, f, indent=4)

def load_chain():
    """Muat blockchain dari file JSON jika ada"""
    if os.path.exists(BLOCKCHAIN_FILE):
        with open(BLOCKCHAIN_FILE, 'r') as f:
            blockchain.chain = json.load(f)
            print(f"[*] Blockchain dimuat dari {BLOCKCHAIN_FILE}")

def get_student_db():
    """Ambil daftar mahasiswa dan public key resmi dari students.json"""
    if os.path.exists(STUDENT_DB_FILE):
        with open(STUDENT_DB_FILE, 'r') as f:
            return json.load(f)
    return {}

# Load data saat server nyala
load_chain()

# --- ENDPOINT ---

@app.route('/mine', methods=['GET'])
def mine():
    # Reward miner otomatis
    blockchain.new_transaction(
        nama="SYSTEM_REWARD", 
        keterangan=f"Reward miner: {MINER_ID}",
        signature="SYSTEM",
        public_key="SYSTEM"
    )
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block['proof'])
    prev_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, prev_hash)
    
    # SIMPAN SETIAP HABIS MINING
    save_chain()
    
    return jsonify({
        'message': "Mining Selesai & Data Disimpan",
        'index': block['index'],
        'transactions': block['transactions'],
        'hash': block['hash']
    }), 200

@app.route('/absen', methods=['POST'])
def add_attendance():
    values = request.get_json()
    required = ['nama', 'keterangan', 'public_key', 'signature']
    
    if not all(k in values for k in required):
        return jsonify({'message': 'Data tidak lengkap'}), 400

    # --- VALIDASI DATABASE KAMPUS (WHITE-LIST) ---
    student_db = get_student_db()
    nama_mhs = values['nama']
    pk_mhs = values['public_key']

    if nama_mhs not in student_db:
        return jsonify({'message': f'Nama {nama_mhs} tidak terdaftar di sistem kampus!'}), 403
    
    if student_db[nama_mhs] != pk_mhs:
        return jsonify({'message': 'Public Key tidak cocok dengan database! Upaya titip absen terdeteksi.'}), 401
    # ----------------------------------------------

    # Validasi Digital Signature (Integritas Data)
    if not verify_signature(pk_mhs, values['signature'], nama_mhs, values['keterangan']):
        return jsonify({'message': 'Signature tidak valid! Data telah dimanipulasi.'}), 401

    index = blockchain.new_transaction(nama_mhs, values['keterangan'], values['signature'], pk_mhs)
    return jsonify({'message': f'Absen sukses, masuk antrian blok {index}'}), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    return jsonify({'chain': blockchain.chain, 'length': len(blockchain.chain)}), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Daftar node tidak ditemukan", 400
    for node in nodes:
        blockchain.register_node(node)
    return jsonify({'message': 'Node tetangga berhasil didaftarkan', 'total_nodes': list(blockchain.nodes)}), 201

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()
    if replaced:
        save_chain() # Simpan jika chain diperbarui dari node lain
        return jsonify({'message': 'Chain diperbarui (Sinkron)', 'new_chain': blockchain.chain}), 200
    return jsonify({'message': 'Chain sudah yang terbaru', 'chain': blockchain.chain}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(port_id))