from service.socket_service import get_recharge_station
import json

def test_recharge_station():
    # Teste com coordenadas válidas
    print("🔹 Teste 1: Procurando posto para (3.0, 4.0)")
    response = get_recharge_station(3.0, 4.0)
    print(json.dumps(response, indent=4, ensure_ascii=False))

    # Teste com coordenadas diferentes
    print("\n🔹 Teste 2: Procurando posto para (6.5, 2.3)")
    response = get_recharge_station(6.5, 2.3)
    print(json.dumps(response, indent=4, ensure_ascii=False))

    # Teste com coordenadas erradas
    print("\n🔹 Teste 3: Testando erro (coordenadas inválidas)")
    response = get_recharge_station("abc", "xyz")
    print(json.dumps(response, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    test_recharge_station()
