from datetime import datetime, timezone
from typing import Dict

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Motor Anti-Fraude API")

# Janela de tempo para identificar uma possível "viagem impossível".
JANELA_FRAUDE_MINUTOS = 60


class Transacao(BaseModel):
    usuario_id: int
    valor: float = Field(gt=0, description="O valor deve ser maior que zero.")
    cidade: str = Field(min_length=2)
    data_hora: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Data/hora ISO 8601; se omitida, usa o horário atual em UTC.",
    )


# Simulação de armazenamento em memória: mantém apenas a última transação aprovada.
historico_usuarios: Dict[int, dict] = {}


def normalizar_data_hora(data_hora: datetime) -> datetime:
    # Interpreta horários sem fuso como UTC para permitir a comparação.
    if data_hora.tzinfo is None:
        return data_hora.replace(tzinfo=timezone.utc)
    return data_hora


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "mensagem": "Motor Anti-Fraude operando normalmente",
    }


@app.post("/analisar")
def analisar_transacao(transacao: Transacao):
    usuario = transacao.usuario_id
    horario_atual = normalizar_data_hora(transacao.data_hora)
    cidade_atual = transacao.cidade.strip()

    # Regra 1: limite de valor financeiro.
    if transacao.valor > 10000.00:
        return {
            "status": "bloqueado",
            "motivo": "Valor excede limite de segurança.",
        }

    # Regra 2: compara com a última transação APROVADA.
    ultima_transacao_aprovada = historico_usuarios.get(usuario)

    if ultima_transacao_aprovada:
        ultima_cidade = ultima_transacao_aprovada["cidade"]
        ultimo_horario = normalizar_data_hora(
            ultima_transacao_aprovada["data_hora"]
        )

        diferenca_minutos = (
            horario_atual - ultimo_horario
        ).total_seconds() / 60

        mudou_de_cidade = ultima_cidade.casefold() != cidade_atual.casefold()
        dentro_da_janela = 0 <= diferenca_minutos <= JANELA_FRAUDE_MINUTOS

        if mudou_de_cidade and dentro_da_janela:
            # Não altera o histórico: a referência continua sendo a última aprovada.
            return {
                "status": "bloqueado",
                "motivo": (
                    "Suspeita de fraude: a última transação aprovada foi em "
                    f"'{ultima_cidade}' e a atual é em '{cidade_atual}'. "
                    f"A diferença está dentro da janela de {JANELA_FRAUDE_MINUTOS} minutos."
                ),
            }

    # Só chega aqui quando a transação foi aprovada: atualiza cidade e horário.
    historico_usuarios[usuario] = {
        "cidade": cidade_atual,
        "data_hora": horario_atual,
    }

    return {
        "status": "aprovado",
        "motivo": "Transação dentro dos padrões normais.",
    }
