# Import das libs e definições necessarias.
import paho.mqtt.client as mqtt
import time
from definitions.definitions2 import cliente_id, user, password, server, port
from hal import temperatura_inicial, incrementa_temperatura, decrementa_temperatura, aquecedor

#CONSTANTE TEMPERATURA IDEAL
TEMPERATURA_IDEAL = 30

# Inicia o status do aquecedor
AQUECEDOR_LIGADO = False

# Pega a temperatura inicial do comodo (MOCK)
TEMPERATURA = temperatura_inicial()

#Estabelece a cliente
cliente = mqtt.Client(cliente_id)

# Realiza autenticação no broker
cliente.username_pw_set(user, password)

# Realiza a conexao
cliente.connect(server, port)

# Função responsavel por pegar o estatus do aquecedor
def get_status_aquecedor(client, user_date, msg):
    global AQUECEDOR_LIGADO
    vetor = msg.payload.decode().split(',')
    AQUECEDOR_LIGADO = aquecedor('on' if vetor[1] == '1' else '0')
    client.publish('v1/' + user + '/things/' + cliente_id + '/response', 'ok,' + vetor[0] + '')

# Quando receber uma mensagem chame a funcao
cliente.on_message = get_status_aquecedor

# Nome do topico para ficar monitorando (Subscribe)
cliente.subscribe('v1/' + user + '/things/' + cliente_id + '/cmd/4')

# Fique monitorando constantemente o topico
cliente.loop_start()

# Publish inicial
cliente.publish('v1/' + user + '/things/' + cliente_id + '/data/2', decrementa_temperatura(TEMPERATURA))

# Responsavel por realizar o publish da temperatura a cada 10 segundos.
while(True):
    if (AQUECEDOR_LIGADO == True and TEMPERATURA < TEMPERATURA_IDEAL):
        TEMPERATURA = incrementa_temperatura(TEMPERATURA)
        cliente.publish('v1/' + user + '/things/' + cliente_id + '/data/2', TEMPERATURA)

    else:
        TEMPERATURA = decrementa_temperatura(TEMPERATURA)
        cliente.publish('v1/' + user + '/things/' + cliente_id + '/data/2', decrementa_temperatura(TEMPERATURA))
    # Necessario por causa do Cayeene
    time.sleep(2)
