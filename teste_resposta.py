import socket


HOST = "145.223.27.42"  # Coloque o IP da VPS
PORT = 8015

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
client.sendall(b"bateria_baixa,100,100")
response = client.recv(1024).decode()

print("Resposta:", response)
client.close()