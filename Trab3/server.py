#!flask/bin/python
from flask import Flask, jsonify, request
import threading, json

app = Flask(__name__)

valid = 0
cod_passagem = 3
cod_hotel = 3
vagas_hotel1 = 20
vagas_hotel2 = 20
vagas_aviao1 = 50
vagas_aviao2 = 50
lock = threading.Lock()

compras_passagem = [
    {
        'id': 1,
        'vagas': 50,
        'tipo_viagem': u'Ida',
        'origem': u'Curitiba',
        'destino': u'Sao Paulo',
        'data_ida': u'10/06/18',
        'data_volta': u'Somente Ida',
        'qtde_pessoas': u'2',
        'numero_cartao': u'123456789',
        'forma_pgto': u'1'
    },
    {
        'id': 2,
        'vagas': 50,
        'tipo_viagem': u'Ida e Volta',
        'origem': u'Curitiba',
        'destino': u'Salvador',
        'data_ida': u'13/06/18',
        'data_volta': u'25/06/18',
        'qtde_pessoas': u'3',
        'numero_cartao': u'987654321',
        'forma_pgto': u'2'
    }
]

compras_hotel = [
    {
        'id': 1,
        'vagas': 20,
        'nome_hotel': u'Palace Del Rey II',
        'nome_destino': u'Salvador',
        'data_entrada': u'10/06/18',
        'data_saida': u'15/06/18',
        'numero_quartos': u'2',
        'qtde_pessoas': u'2',
        'numero_cartao': u'123456789',
        'forma_pgto': u'1'
    },
    {
        'id': 2,
        'vagas': 20,
        'nome_hotel': u'Code Palace X',
        'nome_destino': u'Maceio',
        'data_entrada': u'15/06/18',
        'data_saida': u'23/07/18',
        'numero_quartos': u'3',
        'qtde_pessoas': u'5',
        'numero_cartao': u'987654321',
        'forma_pgto': u'1'
    }
]

########################################################################################
################################  A V I A O   ##########################################
########################################################################################

# mostra todas as vendas de passagens aereas
@app.route('/passagens', methods=['GET'])
def get_compras_passagem():
    return jsonify({'compras_passagem': compras_passagem})

# mostra compras de passagem por id
@app.route('/passagens/<int:compra_id>', methods=['GET'])
def get_passagem(compra_id):
    compra = [compra for compra in compras_passagem if compra['id'] == compra_id]
    try:
        # retorna item indicado
        return jsonify({'compra': compra[0]})
    except:
        # se nao encontrar retorna erro
        return 'Pagina nao encontrada'

# Insere uma nova compra de voo
@app.route('/compra_passagem/', methods=['GET'])
def get_compra_passagem():
    global cod_passagem, vagas_aviao1, vagas_aviao2, valid
    valid = 0
    # inicio do lock
    lock.acquire()
    print("metodo bloqueado")

    # captura dados informados pelo cliente
    tipoViagem = request.args.get('Tipoviagem')
    origem = request.args.get('Origem')
    destino = request.args.get('Destino')
    dataIda = request.args.get('DataIda')
    dataVolta = request.args.get('DataVolta')
    numAviao = request.args.get('NumeroAviao')
    qtde_pessoas = request.args.get('Qtde_pessoas')
    numCartao = request.args.get('Num_cartao')
    formaPgto = request.args.get('Forma_pgto')
    numAviao = int(numAviao)
    qtde_pessoas = int(qtde_pessoas)

    # condicao para verificar qual voo foi selecionado e diminuir numero de assentos disponiveis
    if (numAviao == 1):
        vagas_aviao1 = vagas_aviao1 - qtde_pessoas
    if (numAviao == 2):
        vagas_aviao2 = vagas_aviao2 - qtde_pessoas        

    print("Vagas aviao 1: ", vagas_aviao1)
    print("Vagas aviao 2: ", vagas_aviao2)

    # Verifica disponibilidade de poltronas
    if(int(vagas_aviao1) >= 0 and int(vagas_aviao2) >= 0):
        valid = 1
    else:
        valid = 0

    # coloca dados no json
    if (valid == 1):
        for item in compras_passagem:
            if (item['id'] == numAviao):
                item['vagas'] = item['vagas'] - qtde_pessoas
            else:
                continue
        # fim do lock
        lock.release()
        print("metodo desbloqueado")
        return "Compra do voo realizada com sucesso"
    else:
        # fim do lock
        lock.release()
        print("metodo desbloqueado")
        return "Numero de assentos insuficiente"


########################################################################################
################################  H O T E L   ##########################################
########################################################################################

# mostra todas as reservas de hotel
@app.route('/hoteis', methods=['GET'])
def get_hoteis():
    return jsonify({'hoteis': compras_hotel})

# mostra reservas por id
@app.route('/hoteis/<int:compra_id>', methods=['GET'])
def get_hotel(compra_id):
    compra = [compra for compra in compras_hotel if compra['id'] == compra_id]
    try:
        # retorna item indicado
    	return jsonify({'compra': compra[0]})
    except:
        # se nao encontrar retorna erro
    	return jsonify({'error 404': 'Not found'})

# Insere uma nova reserva de hotel
@app.route('/reserva_hotel/', methods=['GET'])
def get_reserva_hotel():
    # inicio do lock
    lock.acquire()
    print("metodo bloqueado")
    global cod_hotel, vagas_hotel1, vagas_hotel2, valid
    valid = 0

    # captura dados informados pelo cliente
    destino = request.args.get('Destino')
    dataEntrada = request.args.get('DataEntrada')
    dataSaida = request.args.get('DataSaida')
    qtdeQuartos = request.args.get('NumQuartos')
    numHotel = request.args.get('NumHotel')
    qtdePessoas = request.args.get('QtdePessoas')
    numCartao = request.args.get('NumCartao')
    formaPgto = request.args.get('FormaPgto')
    numHotel = int(numHotel)
    qtdeQuartos = int(qtdeQuartos)

    # condicao para verificar qual hotel foi selecionado e diminuir numero de vagas disponiveis
    if (numHotel == 1):
        vagas_hotel1 = vagas_hotel1 - qtdeQuartos
    if (numHotel == 2):
        vagas_hotel2 = vagas_hotel2 - qtdeQuartos        

    print("Vagas hotel 1: ", vagas_hotel1)
    print("Vagas hotel 2: ", vagas_hotel2)

    # Verifica disponibilidade de poltronas
    if(int(vagas_hotel1) >= 0 and int(vagas_hotel2) >= 0):
        valid = 1
    else:
        valid = 0

    # coloca dados no json
    if (valid == 1):
        for item in compras_hotel:
            if (item['id'] == numHotel):
                item['vagas'] = item['vagas'] - qtdeQuartos
            else:
                continue
        # fim do lock
        lock.release()
        print("metodo desbloqueado")
        return "Reserva do hotel realizada com sucesso"
    else:
            # fim do lock
        lock.release()
        print("metodo desbloqueado")
        return "Vagas insificientes para a quantidade solicitada"


# executa o servidor
if __name__ == '__main__':
    app.run(debug=True)