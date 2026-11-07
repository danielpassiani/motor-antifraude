# Motor Anti-Fraude API 🛡️

Uma API REST desenvolvida em Python com FastAPI para simular a análise de transações financeiras e identificar comportamentos suspeitos. O projeto aplica regras simples de negócio, validação de dados e armazenamento temporário em memória.

## 🚀 Tecnologias utilizadas

- **Python 3.11**
- **FastAPI:** criação dos endpoints da API.
- **Pydantic:** validação dos dados recebidos.
- **Pytest:** testes automatizados.
- **Git e GitHub:** versionamento do projeto.

## ⚙️ Regras de negócio

1. **Limite de valor financeiro:** bloqueia transações acima de R$ 10.000.
2. **Mudança de cidade em curto intervalo:** compara a transação com a última transação aprovada do usuário. Se a cidade for diferente e o intervalo for de até 60 minutos, a transação é bloqueada.

### Como funciona o histórico

O sistema guarda somente a última transação **aprovada** de cada usuário, incluindo cidade e data/hora. Uma transação bloqueada não altera o histórico. Dessa forma, novas tentativas continuam sendo comparadas com a última transação aprovada.

A janela temporal pode ser ajustada pela constante `JANELA_FRAUDE_MINUTOS` no arquivo `main.py`.

O campo `data_hora` é opcional. Se não for enviado, a API utiliza o horário atual em UTC. Para informar manualmente, use o formato ISO 8601, por exemplo: `2026-11-07T10:30:00Z`.

## 🛠️ Como executar localmente

Clone o repositório:

```bash
git clone https://github.com/danielpassiani/motor-antifraude.git
cd motor-antifraude
```

Crie e ative um ambiente virtual (opcional, mas recomendado):

```bash
python -m venv venv
```

No Windows:

```bash
venv\\Scripts\\activate
```

Instale as dependências:

```bash
pip install fastapi uvicorn pydantic pytest httpx
```

Inicie a API:

```bash
uvicorn main:app --reload
```

A documentação interativa estará disponível em http://127.0.0.1:8000/docs.

## 🧪 Executar os testes

```bash
pytest -v
```

Os testes verificam o endpoint de saúde, aprovação de transações, limite financeiro, regra de mudança de cidade, preservação do histórico após bloqueio, janela temporal e validação de valor positivo.

## 📌 Observação

Este é um projeto educacional para praticar desenvolvimento backend e regras de negócio. O histórico é mantido em memória e é perdido quando a aplicação é reiniciada; portanto, esta implementação não deve ser utilizada como sistema antifraude de produção.
