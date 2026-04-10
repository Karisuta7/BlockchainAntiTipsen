import hashlib
import json
from time import time
from urllib.parse import urlparse
import requests

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()
        # Create genesis block
        self.new_block(previous_hash='1', proof=100)

    def register_node(self, address):
        """Mendaftarkan node tetangga (Networking)"""
        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            self.nodes.add(parsed_url.path)

    def valid_chain(self, chain):
        """Validasi integritas chain dari node lain"""
        last_block = chain[0]
        current_index = 1
        while current_index < len(chain):
            block = chain[current_index]
            if block['previous_hash'] != self.hash(last_block):
                return False
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False
            last_block = block
            current_index += 1
        return True

    def resolve_conflicts(self):
        """KONSENSUS: Aturan Rantai Terpanjang (Synchronization)"""
        neighbours = self.nodes
        new_chain = None
        max_length = len(self.chain)

        for node in neighbours:
            try:
                response = requests.get(f'http://{node}/chain', timeout=5)
                if response.status_code == 200:
                    length = response.json()['length']
                    chain = response.json()['chain']
                    if length > max_length and self.valid_chain(chain):
                        max_length = length
                        new_chain = chain
            except:
                continue

        if new_chain:
            self.chain = new_chain
            return True
        return False

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = []
        block['hash'] = self.hash(block)
        self.chain.append(block)
        return block

    def new_transaction(self, nama, keterangan, signature, public_key):
        self.current_transactions.append({
            'mahasiswa': nama,
            'status': keterangan,
            'signature': signature,
            'public_key': public_key,
            'timestamp': time()
        })
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        block_copy = block.copy()
        block_copy.pop('hash', None)
        block_string = json.dumps(block_copy, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

def save_to_disk(self):
    with open(f'blockchain_{port_id}.json', 'w') as f: # port_id diambil dari app.py
        json.dump(self.chain, f, indent=4)

def load_from_disk(self):
    try:
        with open(f'blockchain_{port_id}.json', 'r') as f:
            self.chain = json.load(f)
    except FileNotFoundError:
        pass 