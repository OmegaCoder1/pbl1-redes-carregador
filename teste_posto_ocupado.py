from service.socket_service import send_to_container, get_recharge_station
# Exemplo de uso
print(get_recharge_station(4, 5))  # Deve retornar o posto mais próximo disponível
print(get_recharge_station(7, 6))  # Deve retornar outro posto disponível, já que o anterior está ocupado