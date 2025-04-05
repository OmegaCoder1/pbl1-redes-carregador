import time
import math

class StationController:
    def __init__(self):
        """Inicializa as estações de recarga disponíveis."""
        self.charging_stations = {
            "Posto 1": {"x": 18.0, "y": 32.0, "ocupado": False, "tempo_expiracao": {},"id": None, "queue" : []},
            "Posto 2": {"x": 500.0, "y": 708.0, "ocupado": False, "tempo_expiracao": {},"id": None, "queue" : []},
            "Posto 3": {"x": 1280.0, "y": 2202.0, "ocupado": False, "tempo_expiracao": {},"id": None, "queue" : []},
            "Posto 4": {"x": 4000.0, "y": 2190.0, "ocupado": False, "tempo_expiracao": {},"id": None, "queue" : []},
            "Posto 5": {"x": 1200.0, "y": 3120.0, "ocupado": False, "tempo_expiracao": {},"id": None, "queue" : []},
        }



    #FUNCAO PARA RETORNAR TODAS AS STATIONS (MESMO OCUPADAS)
    def get_all_stations(self):
        """Retorna todos os postos."""
        return self.charging_stations.copy()

    def checa_tempo_expirou(self):
        """Libera os carros das estações cujo tempo já expiraram."""
        try:
            for nome in self.charging_stations.keys():
                if self.charging_stations[nome]["queue"] == []:
                    self.charging_stations[nome]["ocupado"] = False
                for id, tempo in self.charging_stations[nome]["tempo_expiracao"].items():
                    #FUNÇAO QUEBRADA NAO ESTA ENTRANDO NESTE FOR
                    if time.time() > tempo:
                        self.remover_reserva_carro(id)
                        return {"status": "sucesso", "mensagem": "Estações expiradas foram liberadas."}
        except Exception as e:
            return {"status": "erro", "mensagem": f"Erro ao liberar estações expiradas: {str(e)}"}

    def remover_reserva_carro(self, id):
        """Libera o carro do posto em que ele está reservado."""
        try:
            for nome, dados in self.charging_stations.items():
                if id in dados["queue"]:
                    dados["queue"].remove(id)
                    dados["tempo_expiracao"].pop(id)
        except Exception as e:
            print(f"Erro ao liberar reserva do carro: {str(e)}")

    def liberar_estacoes_expiradas(self):
        """Libera todas as estações cujos tempos de expiração já passaram."""
        try:
            for nome, dados in self.charging_stations.items():
                # Verifica se a estação está ocupada e se o tempo de expiração já passou
                if dados["ocupado"] and dados["tempo_expiracao"] and time.time() > dados["tempo_expiracao"]:
                    # Libera a estação
                    self.reset_station(nome)
                    print(f"A estação {nome} foi liberada devido ao tempo expirado.")
            return {"status": "sucesso", "mensagem": "Estações expiradas foram liberadas."}
        except Exception as e:
            return {"status": "erro", "mensagem": f"Erro ao liberar estações expiradas: {str(e)}"}



    # FUNCOES PARA RETORNAR OS POSTOS DISPONIVEIS E TAMBEM O POSTO MAIS PROXIMO (JA RESERVA)
    def get_available_stations(self):
        """Retorna os postos disponíveis (não ocupados)."""
        try:
            return {
                nome: dados for nome, dados in self.charging_stations.items()
                if not dados["ocupado"]
            }
        except Exception as e:
            return {
                "status": "erro",
                "mensagem": f"Erro ao obter postos disponíveis: {str(e)}"
            }

    def get_station_mais_proximo(self, x, y,id):
        """Retorna o nome do posto mais próximo (não ocupado) e marca como ocupado por 2 minutos."""
        
        
        menorTempo = 9999999
        for nome, dados_posto in self.charging_stations.items():
            tempo = len(dados_posto["queue"]) * 120 + calcular_distancia(x, y, dados_posto["x"], dados_posto["y"])
            if tempo < menorTempo:
                menorTempo = tempo
                station_mais_proximo = nome
            
        self.set_station_occupied(station_mais_proximo,id)  #  Marca o posto como ocupado


            
        return {
            "status": "sucesso",
            "mensagem": f"O posto mais próximo disponível é: {station_mais_proximo}"
        }

    ###########################################################################################

    # DEFINE O STATION COMO OCUPADO ############################################################
    def set_station_occupied(self, station_name, id):
        """Marca um posto como ocupado por 2 minutos."""
        try:
            if station_name in self.charging_stations:
                print(f"mudou o status de : {station_name} para true")
                self.charging_stations[station_name]["ocupado"] = True
                self.charging_stations[station_name]["tempo_expiracao"][id] = time.time() + 120  # 2 minutos
                self.charging_stations[station_name]["reservation_data"] = time.time()
                self.charging_stations[station_name]["id"] = id
                self.charging_stations[station_name]["queue"].append(id)
                print(f"print de todos os postos atuais: {self.charging_stations}")
        except Exception as e:
            print(f"Erro ao marcar posto como ocupado: {str(e)}")
            
    ###########################################################################################

    # DESOCUPAR UMA STATION PELO NOME DELA (USAR COMO ADM PARA LIBERAR MANUALMENTE A ESTAÇÃO)
    def reset_station(self, station_name):
        """Libera um posto manualmente."""
        try:
            if station_name in self.charging_stations:
                self.charging_stations[station_name]["ocupado"] = False
                self.charging_stations[station_name]["tempo_expiracao"] = {}
                self.charging_stations[station_name]["queue"] = []
                self.charging_stations[station_name]["reservation_data"] = None
                self.charging_stations[station_name]["id"] = None
        except Exception as e:
            print(f"Erro ao liberar a estação: {str(e)}")
            
    ###########################################################################################

    # RETORNA TODAS AS ESTAÇÕES OCUPADAS POR UM ID ############################
    def get_stations_by_id(self, id_usuario):
        """Retorna todas as estações ocupadas por um determinado ID e a mensagem com a estação mais próxima."""

        try:
            # Filtra as estações ocupadas com o id_usuario correspondente
            stations_ocupadas = {
                nome: dados for nome, dados in self.charging_stations.items()
                if dados.get("ocupado") and id_usuario in dados.get("queue")
            }

            if stations_ocupadas:
                # Considerando a primeira estação ocupada como a mais próxima
                station_mais_proximo = list(stations_ocupadas.keys())[0]
                return {
                    "status": "sucesso",
                    "mensagem": f"Postos reservados: {station_mais_proximo} (você é o {self.charging_stations[station_mais_proximo]["queue"].index(id_usuario)+1}º da fila), {stations_ocupadas}"
                }
            else:
                # Caso não haja estações ocupadas para o usuário
                return {
                    "status": "erro",
                    "mensagem": "Nenhuma estação ocupada encontrada para o usuário."
                }
        except Exception as e:
            return {
                "status": "erro",
                "mensagem": f"Erro inesperado: {str(e)}"
            }
    ###########################################################################################

    # LIBERA TODAS AS ESTAÇÕES OCUPADAS POR UM ID ##############################################
    def release_stations_by_id(self, id_usuario):
        """Libera todas as estações ocupadas por um determinado ID e retorna status no formato JSON."""
        try:
            stations_lib = []  # Lista para armazenar os nomes das estações liberadas

            for nome, dados in self.charging_stations.items():
                if dados.get("ocupado") and dados.get("id") == id_usuario:
                    self.reset_station(nome)  # Usa a função existente para liberar o posto
                    stations_lib.append(nome)

            if stations_lib:
                return {
                    "status": "sucesso",
                    "mensagem": f"As estações liberadas para o usuário {id_usuario} são: {', '.join(stations_lib)}"
                }
            else:
                # Caso não haja estações ocupadas para o usuário
                return {
                    "status": "erro",
                    "mensagem": "Nenhuma estação ocupada encontrada para o usuário."
                }
        except Exception as e:
            return {
                "status": "erro",
                "mensagem": f"Erro inesperado ao liberar as estações: {str(e)}"
            }
    ###########################################################################################

    # FUNCAO PARA LIBERAR TODOS OS POSTOS, SEM PRECISAR DE ID (USADO COMO ADM)
    def release_all_stations(self):
        """Libera todos os postos ocupados, sem precisar de ID de usuário e retorna status no formato JSON."""
        try:
            stations_lib = []  # Lista para armazenar os nomes das estações liberadas

            for nome, dados in self.charging_stations.items():
                if dados.get("ocupado"):
                    self.reset_station(nome)  # Usa a função existente para liberar o posto
                    stations_lib.append(nome)

            if stations_lib:
                return {
                    "status": "sucesso",
                    "mensagem": f"As estações liberadas são: {', '.join(stations_lib)}"
                }
            else:
                # Caso não haja estações ocupadas
                return {
                    "status": "erro",
                    "mensagem": "Nenhuma estação ocupada foi encontrada para liberar."
                }
        except Exception as e:
            return {
                "status": "erro",
                "mensagem": f"Erro inesperado ao liberar todas as estações: {str(e)}"
            }

# funções gerais:
def calcular_distancia(x1, y1, x2, y2):
    """Calcula a distância Euclidiana entre dois pontos."""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)