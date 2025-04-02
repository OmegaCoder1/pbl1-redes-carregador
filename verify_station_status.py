import socket

HOST = "145.223.27.42"  # IP da VPS
PORT = 8015

def send_request(message):
    try:
        # Cria o socket de comunicação
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Conecta ao servidor
        client.connect((HOST, PORT))
        
        # Envia a mensagem para o servidor
        client.sendall(message.encode())
        
        # Recebe a resposta do servidor
        response = client.recv(1024).decode()
        
        print("Resposta:", response)
        
        # Fecha a conexão
        client.close()
        
        return response
    except Exception as e:
        print(f"Erro ao enviar a solicitação: {str(e)}")
        return None

# Mensagem que será enviada para o servidor
message = "liberar_estacoes_expiradas"

# Envia a solicitação
response = send_request(message)
