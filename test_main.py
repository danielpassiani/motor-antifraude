from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from main import app, historico_usuarios

client = TestClient(app)


@pytest.fixture(autouse=True)
def limpar_historico():
    historico_usuarios.clear()
    yield
    historico_usuarios.clear()


def enviar(usuario, cidade, horario, valor=100.0):
    return client.post(
        "/analisar",
        json={
            "usuario_id": usuario,
            "valor": valor,
            "cidade": cidade,
            "data_hora": horario,
        },
    )


def test_health_check_deve_retornar_ok():
    resposta = client.get("/")
    assert resposta.status_code == 200
    assert resposta.json()["status"] == "ok"


def test_primeira_transacao_deve_ser_aprovada():
    resposta = enviar(1, "São Paulo", "2026-11-07T10:00:00Z")
    assert resposta.status_code == 200
    assert resposta.json()["status"] == "aprovado"


def test_valor_acima_do_limite_deve_ser_bloqueado():
    resposta = enviar(2, "São Paulo", "2026-11-07T10:00:00Z", valor=15000)
    assert resposta.status_code == 200
    assert resposta.json()["status"] == "bloqueado"
    assert 2 not in historico_usuarios


def test_mudanca_de_cidade_dentro_da_janela_deve_ser_bloqueada():
    assert enviar(3, "São Paulo", "2026-11-07T10:00:00Z").json()["status"] == "aprovado"
    resposta = enviar(3, "Curitiba", "2026-11-07T10:30:00Z")
    assert resposta.json()["status"] == "bloqueado"


def test_transacao_bloqueada_nao_atualiza_historico():
    enviar(4, "São Paulo", "2026-11-07T10:00:00Z")
    enviar(4, "Curitiba", "2026-11-07T10:30:00Z")

    assert historico_usuarios[4]["cidade"] == "São Paulo"
    assert historico_usuarios[4]["data_hora"] == datetime(
        2026, 11, 7, 10, 0, tzinfo=timezone.utc
    )


def test_terceira_tentativa_na_cidade_bloqueada_tambem_e_bloqueada():
    enviar(5, "São Paulo", "2026-11-07T10:00:00Z")
    segunda = enviar(5, "Curitiba", "2026-11-07T10:20:00Z")
    terceira = enviar(5, "Curitiba", "2026-11-07T10:25:00Z")

    assert segunda.json()["status"] == "bloqueado"
    assert terceira.json()["status"] == "bloqueado"
    assert historico_usuarios[5]["cidade"] == "São Paulo"


def test_mudanca_de_cidade_fora_da_janela_e_aprovada():
    enviar(6, "São Paulo", "2026-11-07T10:00:00Z")
    resposta = enviar(6, "Curitiba", "2026-11-07T11:01:00Z")

    assert resposta.json()["status"] == "aprovado"
    assert historico_usuarios[6]["cidade"] == "Curitiba"


def test_mesma_cidade_dentro_da_janela_e_aprovada():
    enviar(7, "São Paulo", "2026-11-07T10:00:00Z")
    resposta = enviar(7, "São Paulo", "2026-11-07T10:10:00Z")
    assert resposta.json()["status"] == "aprovado"


def test_valor_zero_e_rejeitado_pela_validacao():
    resposta = enviar(8, "São Paulo", "2026-11-07T10:00:00Z", valor=0)
    assert resposta.status_code == 422
