# Motor Anti-Fraude API 🛡️

Uma API RESTful desenvolvida em Python (FastAPI) para analisar transações financeiras e detectar padrões de fraude em tempo real. O sistema utiliza validação rigorosa de dados e simula um cache em memória para rastrear comportamentos suspeitos, como a regra de "Viagem Impossível".

## 🚀 Tecnologias Utilizadas
* **Python 3.11**
* **FastAPI:** Framework assíncrono de alta performance para a construção das rotas.
* **Pydantic:** Tipagem estática e validação rigorosa dos payloads.
* **Pytest:** Bateria de testes unitários automatizados para garantir a estabilidade das regras de negócio.

## ⚙️ Regras de Negócio Implementadas
1. **Limite de Valor Financeiro:** Bloqueio imediato de transações que excedem o teto de segurança operacional (R$ 10.000).
2. **Viagem Impossível (Behavioral Tracking):** Cruzamento de dados de localização do usuário. Bloqueia transações sequenciais aprovadas em cidades diferentes em um curto espaço de tempo.

## 🛠️ Como Executar o Projeto Localmente

1. Clone o repositório:
```bash
git clone https://github.com/danielpassiani/motor-antifraude.git
cd motor-antifraude
