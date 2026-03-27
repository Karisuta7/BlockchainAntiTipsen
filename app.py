import sys
from flask import Flask, jsonify, request
from blockchain import Blockchain
from signature import verify_signature 

app = Flask(__name__)
blockchain = Blockchain()

# ID unik miner berdasarkan Port agar tidak tertukar
port_id = sys.argv[1] if len(sys.argv) > 1 else "5000"
MINER_ID = f"Admin_Node_{port_id}"

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
    return jsonify({
        'message': "Mining Selesai",
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

    if not verify_signature(values['public_key'], values['signature'], values['nama'], values['keterangan']):
        return jsonify({'message': 'Signature tidak valid! Titip absen terdeteksi.'}), 401

    index = blockchain.new_transaction(values['nama'], values['keterangan'], values['signature'], values['public_key'])
    return jsonify({'message': f'Absen sukses, masuk antrian blok {index}'}), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    return jsonify({'chain': blockchain.chain, 'length': len(blockchain.chain)}), 200

# --- TAMBAHAN ENDPOINT MULTI-NODE (NETWORKING) ---

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
        return jsonify({'message': 'Chain diperbarui (Sinkron)', 'new_chain': blockchain.chain}), 200
    return jsonify({'message': 'Chain sudah yang terbaru', 'chain': blockchain.chain}), 200

if __name__ == '__main__':
    # Biar bisa jalanin: python app.py 5000, 5001, 5002
    app.run(host='0.0.0.0', port=int(port_id))