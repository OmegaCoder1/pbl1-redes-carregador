import time
import math

class StationController:
    def _init_(self):
        """Inicializa as estações de recarga disponíveis."""
        self.charging_stations = {
            "Posto 1": {"x": 2.0, "y": 3.0, "ocupado": False, "tempo_expiracao": None,"id": None, "reservation_data": None},
            "Posto 2": {"x": 5.0, "y": 7.0, "ocupado": False, "tempo_expiracao": None,"id": None, "reservation_data": None},
            "Posto 3": {"x": 8.0, "y": 2.0, "ocupado": False, "tempo_expiracao": None,"id": None, "reservation_data": None},
            "Posto 4": {"x": 1.0, "y": 9.0, "ocupado": False, "tempo_expiracao": None,"id": None, "reservation_data": None},
            "Posto 5": {"x": 6.0, "y": 5.0, "ocupado": False, "tempo_expiracao": None,"id": None, "reservation_data": None},
        }
        


    #FUNCOES PARA RETORNAR OS POSTOS DISPONIVEIS E TAMBEM O POSTO MAIS PROXIMA (JA RESERVA)
    def get_available_stations(self):
        """Retorna os postos disponíveis (não ocupados)."""
        return {
            nome: dados for nome, dados in self.charging_stations.items()
            if not dados["ocupado"] or (dados["tempo_expiracao"] and time.time() > dados["tempo_expiracao"])
        }
        
        
    def get_station_mais_proximo(self, x, y,id):
        """Retorna o nome do posto mais próximo (não ocupado) e marca como ocupado por 2 minutos."""
        
        postos_disponiveis = self.get_available_stations()  #  Obtém os postos disponíveis apenas uma vez
        
        if not postos_disponiveis:  #  Se não houver postos disponíveis, retorna None
            return None  

        station_mais_proximo = min(
            postos_disponiveis,  #  Agora usa a lista já obtida
            key=lambda nome: calcular_distancia(x, y, self.charging_stations[nome]["x"], self.charging_stations[nome]["y"])
        )
        
        self.set_station_occupied(station_mais_proximo,id)  #  Marca o posto como ocupado
        
        return {
            "status": "sucesso",
            "mensagem": f"O posto mais próximo disponível é: {station_mais_proximo}"
        }
        
    ###########################################################################################




    
    
    #DEFINE O STATION COMO OCUPADO ############################################################
    def set_station_occupied(self, station_name,id):
        """Marca um posto como ocupado por 2 minutos."""
        if station_name in self.charging_stations:
            print(f"mudou o status de : {station_name} para true")
            self.charging_stations[station_name]["ocupado"] = True
            self.charging_stations[station_name]["tempo_expiracao"] = time.time() + 120  # 2 minutos
            self.charging_stations[station_name]["reservation_data"] = time.time()
            self.charging_stations[station_name]["id"] = id
            print(f"print de todos os postos atuais: {self.charging_stations}")
            
    ###########################################################################################





    # DESOCUPAR UMA STATION PELO NOME DELA (USAR COMO ADM PARA LIBERAR MANUALMENTE A ESTAÇÃO)
    def reset_station(self, station_name):
        """Libera um posto manualmente."""
        if station_name in self.charging_stations:
            self.charging_stations[station_name]["ocupado"] = False
            self.charging_stations[station_name]["tempo_expiracao"] = None
            self.charging_stations[station_name]["reservation_data"] = None
            self.charging_stations[station_name]["id"] = None
            
    ###########################################################################################
    
    
    
    
    
    # RETORNA TODAS AS ESTAÇÕES OCUPADAS POR UM ID ############################
    def get_stations_by_id(self, id_usuario):
        """Retorna todas as estações ocupadas por um determinado ID."""
        return {
            nome: dados for nome, dados in self.charging_stations.items()
            if dados.get("ocupado") and dados.get("id") == id_usuario
        }
    ###########################################################################################
    
    

    # LIBERA TODAS AS ESTAÇÕES OCUPADAS POR UM ID ##############################################
    def release_stations_by_id(self, id_usuario):
        """Libera todas as estações ocupadas por um determinado ID."""
        for nome, dados in self.charging_stations.items():
            if dados.get("ocupado") and dados.get("id") == id_usuario:
                self.reset_station(nome)  # Usa a função existente para liberar o posto
    ###########################################################################################
    
    #FUNCAO PARA LIBERAR TODOS OS POSTOS, SEM PRECISAR DE ID (USADO COMO ADM)
    def release_all_stations(self):
        """Libera todos os postos ocupados, sem precisar de ID de usuário."""
        for nome, dados in self.charging_stations.items():
            if dados.get("ocupado"):
                self.reset_station(nome)  # Usa a função existente para liberar o posto
                return "TODOS LIBERADOS"













#funcoes gerais:
def calcular_distancia(x1, y1, x2, y2):
    """Calcula a distância Euclidiana entre dois pontos."""
    return math.sqrt((x2 - x1) * 2 + (y2 - y1) * 2)