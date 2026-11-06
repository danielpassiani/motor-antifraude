from fastapi.testclient import TestClient
from main import app

# Criamos um "cliente falso" para disparar requisições contra a nossa API
client = TestClient(app)

def test_health_check_deve_retornar_ok():
    resposta = client.get("/")
    # A palavra 'assert' (afirmar) força o teste a falhar se a condição não for verdadeira
    assert resposta.status_code == 200
    assert resposta.json()["status"] == "ok"

def test_transacao_normal_deve_ser_aprovada():
    payload = {
        "usuario_id": 99,
        "valor": 150.50,
        "cidade": "São Paulo"
    }
    resposta = client.post("/analisar", json=payload)
    
    assert resposta.status_code == 200
    assert resposta.json()["status"] == "aprovado"

def test_transacao_valor_alto_deve_ser_bloqueada():
    payload = {
        "usuario_id": 100,
        "valor": 15000.00,  # Valor acima do limite de 10.000 da nossa regra
        "cidade": "São Paulo"
    }
    resposta = client.post("/analisar", json=payload)
    
    assert resposta.status_code == 200
    assert resposta.json()["status"] == "bloqueado"