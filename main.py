from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Motor Anti-Fraude API")

class Transacao(BaseModel):
    usuario_id: int
    valor: float
    cidade: str

# 1. Simulação de Banco de Dados em Memória (Cache)
# Em produção real, utilizaríamos o Redis para isso.
historico_usuarios = {}

@app.get("/")
def health_check():
    return {"status": "ok", "mensagem": "Motor Anti-Fraude operando normalmente"}

@app.post("/analisar")
def analisar_transacao(transacao: Transacao):
    usuario = transacao.usuario_id
    
    # Regra 1: Limite de valor financeiro
    if transacao.valor > 10000.00:
        return {"status": "bloqueado", "motivo": "Valor excede limite de segurança."}
    
    # Regra 2: Verificação de "Viagem Impossível" (Comportamento)
    # Verifica se o usuário já tem histórico e se a cidade mudou repentinamente
    if usuario in historico_usuarios:
        ultima_cidade = historico_usuarios[usuario]["cidade"]
        
        if ultima_cidade != transacao.cidade:
            # Atualiza o histórico antes de bloquear para registrar a tentativa
            historico_usuarios[usuario] = {"cidade": transacao.cidade}
            return {
                "status": "bloqueado", 
                "motivo": f"Suspeita de fraude: transação anterior foi em '{ultima_cidade}' e a atual em '{transacao.cidade}'."
            }
    
    # 3. Atualizar o histórico com a transação aprovada
    historico_usuarios[usuario] = {"cidade": transacao.cidade}
    
    return {"status": "aprovado", "motivo": "Transação dentro dos padrões normais."}