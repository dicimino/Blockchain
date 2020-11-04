import datetime
import hashlib
import json
from flask import Flask, jsonify

# Parte 1 , criar um Blockchain

class Blockchain:
    def __init__(self):
        self.chain = []                                         # Declara a cadeia como uma lista/array
        self.create_block(nonce = 1, previous_hash='0')
        
    def create_block(self,nonce,previous_hash):                 # Utilizado para criar o bloco gênesis
        index       = len(self.chain) + 1
        hora_inicial = datetime.datetime.now()
        timestamp   = str(hora_inicial)
        
        block = {'index': index,                                # O índice, ou número do bloco
                 'timestamp': str(timestamp),                   # Carimbo de tempo
                 'nonce': nonce,                                # Prova do quebra-cabeça criptográfico
                 'hash_anterior': previous_hash,                # Hash anterior
                 'hash_atual' :   ( hashlib.sha256(str( str(index) + str(timestamp) + str(nonce) + str(previous_hash)  ).encode()).hexdigest() ),                             # Hash atual
                 'dados' : str(datetime.datetime.now() - hora_inicial) # Tempo para calcular o digest
                 }                    
        self.chain.append(block)                                # Adiciona o bloco à cadeia chain
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
                    
    
    def minerar_bloco(self,previous_hash):                      # Mineração do bloco (Proof of Work - PoW / ou prova de trabalho)
        nonce   = 1
        check_proof = False
        index       = len(self.chain) + 1
        hora_inicial = datetime.datetime.now()
        timestamp   = str(hora_inicial)
        while check_proof is False:
            hash_operation = hashlib.sha256(str(  str(index) + str(timestamp) + str(nonce) + str(previous_hash)).encode()).hexdigest()
            if hash_operation[:7] == '0000000':                 # Verifica se os n caracteres à esquerda são 0 - variado entre 4 e 7 zeros.
                check_proof = True
            else:
                nonce += 1 
        block = {'index': index,                                # O índice, ou número do bloco
                 'timestamp': str(timestamp),                   # Carimbo de tempo
                 'nonce': nonce,                                # Prova do quebra-cabeça criptográfico
                 'hash_anterior': previous_hash,                # Hash anterior
                 'hash_atual' :   hash_operation,               # Hash atual
                 'dados' : str(datetime.datetime.now() - hora_inicial) # Tempo para calcular o digest
                }                    
        self.chain.append(block)                                # Adiciona o bloco à cadeia chain
        return block
    
    
    def hash(self,block):
        encoded_block = json.dumps(block,sort_keys=True).encode()   # Como o bloco é um dicionário, passar ele para json
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self,chain):
        previous_block = chain[0]                                   #bloco anterior
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['hash_anterior'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['nonce']
            nonce = block['nonce']
            hash_operation = hashlib.sha256(str(nonce**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
    

app = Flask(__name__)
#Adicionada a linha abaixo por problemas na importação do Flask.
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

blockchain = Blockchain()                                   # Instacionar o Blockchain
@app.route('/mine_block',methods = ['GET'])

def mine_block():
    previous_block = blockchain.get_previous_block()        # Instancinar o bloco anterior
    previous_hash = previous_block['hash_atual']
    block = blockchain.minerar_bloco(previous_hash)
    response = {'mensagem'      : 'Bloco minerado com sucesso!',
                'index'         : block['index'],
                'timestamp'     : block['timestamp'],
                'nonce'         : block['nonce'],
                'hash_anterior' : block['hash_anterior'],
                'hash_atual'    : block['hash_atual'],
                'dados'         : block['dados']}
    return jsonify(response), 200

@app.route('/get_chain',methods = ['GET'])
def get_chain():
    response = {'chain'     : blockchain.chain,
                'Tamanho'   : len(blockchain.chain)}
    return jsonify(response),200

@app.route('/is_valid',methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message' : 'O blockchain é válido'}
    else:
        response = {'message' : 'O blockchain não é válido'}
    return jsonify(response), 200

app.run(host = '0.0.0.0', port=5000)
    
    
    
    
    
    
    
    