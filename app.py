from flask import Flask, jsonify, request
from blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

MINER_ID = "Dosen_atau_Admin_Sistem"

@app.route('/mine', methods=['GET'])
def mine():
   
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block['proof'])

   
    blockchain.new_transaction(
        nama_mahasiswa="SYSTEM_REWARD", 
        keterangan=f"Hadiah 1 Poin untuk Miner {MINER_ID}"
    )

    
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "Blok Absensi Berhasil Dibuat!",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'hash': block['hash']
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    
    required = ['nama', 'keterangan']
    if not all(k in values for k in required):
        return 'Data tidak lengkap', 400

    index = blockchain.new_transaction(values['nama'], values['keterangan'])
    return jsonify({'message': f'Data absen {values["nama"]} masuk antrian Blok {index}'}), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    return jsonify({'chain': blockchain.chain, 'length': len(blockchain.chain)}), 200

if __name__ == '__main__':
    app.run(port=5000)

@app.route('/', methods=['GET'])
def home():
    return "API Blockchain Absensi Aktif! Gunakan /chain untuk melihat data atau /mine untuk mining."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)