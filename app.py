from flask import Flask, jsonify, request
from blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

MINER_ID = "Admin_Kampus_01"

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'API Blockchain Absensi Aktif!',
        'endpoints': {
            '/chain': 'Melihat seluruh rantai blok',
            '/mine': 'Melakukan mining blok baru',
            '/transactions/new': 'Menambah data absen baru (POST)'
        }
    }), 200

@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block['proof'])


    blockchain.new_transaction(
        nama="SYSTEM_REWARD", 
        keterangan=f"Reward 1 Poin diberikan ke {MINER_ID}"
    )
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "Blok Berhasil Di-Mine!",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'hash': block['hash'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['nama', 'keterangan']
    if not all(k in values for k in required):
        return 'Data tidak lengkap', 400

    signature = values.get('signature', 'NONE')

    index = blockchain.new_transaction(values['nama'], values['keterangan'], signature)
    return jsonify({'message': f'Absen {values["nama"]} masuk antrian Blok {index}'}), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    return jsonify({
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }), 200

if __name__ == '__main__':
  
    app.run(host='0.0.0.0', port=5000, debug=True)