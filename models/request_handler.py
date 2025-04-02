import json
# nao to usando mais o socket (pois nao vamos conectar a outra imagem) from service.socket_service import send_to_container, get_recharge_station
from controllers.station_controller import StationController
server = StationController()

class RequestHandler:
    @staticmethod
    def process_request(data):
        
        """
        Processa os dados recebidos e retorna uma resposta apropriada.
        A mensagem é dividida em comando (antes da vírgula) e dados adicionais (após a vírgula).
        """
        print(f"Data recebido pelo RequestHandler: {data}")
        
        # Divida a mensagem em partes (comando, valores)
        parts = data.split(',')
        
        # A primeira parte é o comando
        command = parts[0].strip().lower()

        # Se houver mais de uma parte, as coordenadas são extraídas
        if len(parts) > 1:
            try:
                # Converte as coordenadas X e Y para float
                x = float(parts[1].strip())
                y = float(parts[2].strip()) if len(parts) > 2 else None
                print(f"valoresde x e y : {x} {y}")
            except ValueError:
                return {"status": "erro", "mensagem": "Coordenadas inválidas."}
        else:
            x, y = None, None

        # Processa o comando e executa a ação correspondente
        if command == "low_battery":
            print('chegou no coando de bateria')
            # Se a coordenada Y não for fornecida, use valores padrões
            if x is not None and y is not None:
                print(f"chamou o get_recharge_station")
                return server.get_station_mais_proximo(x, y,parts[3])
            else:
                return {"status": "erro", "mensagem": "Coordenadas de localização não fornecidas."}



        #funcao par retornar todas as reservas de um usuario
        elif command == "all_station_id":
            #recebe o parametor all_staion_id + o id do usuario para buscar por estacoes reservadas
            return server.get_stations_by_id(parts[1])
        ##################################################

        
        
        
        #funcoes para remover o ocupado das estacoes, podendo ser por ID ou geral
        elif command == "release_stations_by_id":
            #recebe o parametor release_stations_by_id + o id do usuario para remover todos os postos alugados por ele
            return server.release_stations_by_id(parts[1])
        

        elif command == "release_all_stations":
            #recebe o parametor release_stations_by_id + o id do usuario para remover todos os postos alugados por ele
            return server.release_all_stations()
        
        ##################################################
        elif command == "liberar_estacoes_expiradas":
            #recebe o parametro verify_reservation_status + o id do usuario para verificar se ele tem alguma reserva
            return server.liberar_estacoes_expiradas()




        elif command == "gerar_pagamento":
            return {"status": "sucesso", "mensagem": "Pagamento PIX gerado com sucesso!"}
        
        elif command =="confirmar_posto":
            return {"status": "sucesso", "mensagem": "teste"}

        else:
            return {"status": "erro", "mensagem": "Comando não reconhecido"}
