from flask import Flask, jsonify, request
from blockchain import Blockchain
from signature import verify_signature 

app = Flask(__name__)
blockchain = Blockchain()

MINER_ID = "Admin_Kampus_01"

@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block['proof'])

    # Reward miner
    blockchain.new_transaction(
        nama="SYSTEM_REWARD", 
        keterangan=f"Reward miner: {MINER_ID}",
        signature="SYSTEM",
        public_key="SYSTEM"
    )
    
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
    
    # Cek input
    required = ['nama', 'keterangan', 'public_key', 'signature']
    if not all(k in values for k in required):
        return jsonify({'message': 'Data tidak lengkap'}), 400

    # Verifikasi signature (Filter Keamanan)
    is_valid = verify_signature(
        values['public_key'],
        values['signature'],
        values['nama'],
        values['keterangan']
    )

    if not is_valid:
        # Tolak kalau data dimanipulasi (Anti-Titip)
        return jsonify({'message': 'Signature tidak valid! Gagal absen.'}), 400

    # Masuk ke antrian kalau valid
    index = blockchain.new_transaction(
        values['nama'], 
        values['keterangan'], 
        values['signature'],
        values['public_key']
    )
    
    return jsonify({'message': f'Absen {values["nama"]} sukses, masuk blok {index}'}), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    return jsonify({
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
