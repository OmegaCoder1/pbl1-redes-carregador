import socket
from models.request_handler import RequestHandler
from views.response_view import ResponseView

class ServerController:
    def __init__(self, host="0.0.0.0", port=8016):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        print(f"[*] Servidor rodando na porta {self.port}")

    def start(self):
        """
        Mantém o servidor rodando e processando conexões.
        """
        while True:
            conn, addr = self.server.accept()
            print(f"[+] Conexão recebida de {addr}")

            data = conn.recv(1024).decode()
            print(f"[>] Dados recebidos: {data}")

            response_data = RequestHandler.process_request(data)
            response_json = ResponseView.format_response(response_data)

            conn.send(response_json.encode())
            conn.close()
