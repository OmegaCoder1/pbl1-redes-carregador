import socket
import json

HOST = "0.0.0.0"
PORT = 8015  # Pode mudar se quiser

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

print(f"[*] Servidor rodando na porta {PORT}")

while True:
    conn, addr = server.accept()
    print(f"[+] Conexão recebida de {addr}")

    data = conn.recv(1024).decode()
    print(f"[>] Dados recebidos: {data}")

    response = json.dumps({"status": "sucesso", "mensagem": "Recebido com sucesso!"})
    conn.send(response.encode())

    conn.close()
