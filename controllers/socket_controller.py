

class SocketController:
    def __init__(self, host: str, port: int):
        from service.socket_service import get_recharge_station
        self.socket_service = get_recharge_station(host, port)

    def handle_request(self, message: str):
        # Chama o service para enviar a mensagem e receber a resposta
        response = self.socket_service.send_to_container(message)
        return None




if __name__ == "__main__":
    # Exemplo de como usar o Controller
    controller = SocketController('145.223.27.42', 8016)
    response = controller.handle_request("bateria_baixa")
    print(response)
