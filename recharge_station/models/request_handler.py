import json

class RequestHandler:
    @staticmethod
    def process_request(data):
        """
        Processa os dados recebidos e retorna uma resposta apropriada.
        """
        if data.lower() == "bateria baixa":
            return {"status": "alerta", "mensagem": "Posto de recarga mais próximo: Av. Central, 123"}
        elif data.lower() == "gerar pagamento":
            return {"status": "sucesso", "mensagem": "Pagamento PIX gerado com sucesso!"}
        else:
            return {"status": "erro", "mensagem": "Comando não reconhecido"}
