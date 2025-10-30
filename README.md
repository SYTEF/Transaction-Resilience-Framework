#Transaction Resilience Framework (MVP)

Este projeto é um **MVP (Produto Mínimo Viável)** de um framework de automação focado em garantir a **Resiliência da Transação** — um pilar crítico no negócio de Pagamentos e Máquinas POS da Stone.

---

## 2. O Problema de Negócio e a Solução

### 2.1. O Conhecimento da Dor (My Unique Value)

Com base na minha experiência com QA de Hardware, a falha mais custosa para o empreendedor é a **perda de venda devido a falhas de comunicação** (sinal 4G/Wi-Fi ruim, lentidão do banco emissor).

* **O problema:** O POS (Maquininha) envia a transação, e o Backend da Stone espera. Se o banco parceiro demora demais, o sistema trava ou fica lento, prejudicando o cliente.
* **A Solução (Resiliência):** Um QA Engineer III precisa garantir que o sistema da Stone seja **resiliente** e desista da transação rapidamente em caso de falha externa, retornando um erro limpo ao POS.

### 2.2. A Estratégia de Qualidade

Escolhemos a **Automação de API** porque ela é a camada mais rápida e escalável para se integrar ao **CI/CD** (Integração Contínua), garantindo que nenhuma mudança de código quebre a resiliência do sistema.

* **Ferramenta Chave:** O uso de **Mockoon** (Mock Server) permite simular ambientes de terceiros (Bancos) de forma controlada, o que é fundamental para testar falhas sem depender de ambientes reais instáveis.

## 3. Cenários e Validação (O que foi Automatizado)

O framework foi configurado para validar 3 comportamentos críticos (o foco de um Pleno/Sênior).

| Teste | Objetivo Estratégico | Comportamento Esperado | Resultado |
| :--- | :--- | :--- | :--- |
| **1. `test_approved_success`** | Validação funcional do Happy Path. | Status HTTP 200, Status no JSON: APPROVED. | ✅ PASSOU |
| **2. `test_handles_bank_timeout`** | **Resiliência:** Simular lentidão de 10s do Banco (problema de sinal do POS) e forçar o sistema Stone a dar *timeout* em **5 segundos**. | O teste deve falhar por `Timeout` (o que é um SUCESSO de resiliência). | ✅ PASSOU |
| **3. `test_handles_contract_error`** | **Estratégia de Contrato:** Simular uma quebra de API (o Banco envia `"estado"` em vez de `"status"`). | O teste deve falhar por `KeyError` no JSON, **detectando a quebra de contrato**. | ✅ PASSOU |

## 4. Próximos Passos (Roadmap de 6 Meses - Visão Engineer III)

Este MVP será expandido com o meu compromisso de crescimento (Live the Ride) e foco em eficiência (Own It):

1.  **Integração CI/CD Imediata:** Configurar o **GitHub Actions** para rodar este `pytest` em cada *push* de código, estabelecendo um "Quality Gate" de Resiliência para a squad de Pagamentos.
2.  **Testes de Contrato (PactFlow):** Evoluir o `Cenário 3` para usar o PactFlow (ou similar) para validar o *schema* de APIs de forma formal e antecipada, protegendo a comunicação com Pagar.me e Ton.
3.  **Performance e Escala:** Adicionar testes de carga (com JMeter/Locust) para garantir que a API de Transação não apenas funciona, mas suporta milhões de chamadas, mantendo a latência baixa.
4.  **Mentoria de Conhecimento:** Usar minha experiência em QA de Hardware para guiar os Desenvolvedores e QAs na criação de novos cenários que reflitam as falhas do mundo real (caminhões, túneis, bairros com 3G, etc.).

## 5. Setup Técnico e Execução

### Pré-requisitos
* Python 3.8+
* **Mockoon Desktop** (Servidor Mock)
* Git

### Instruções

1.  **Clone o Repositório:** `https://github.com/SYTEF/Transaction-Resilience-Framework.git`
2.  **Instale Dependências:** (No Terminal/PowerShell)
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # Ativa o ambiente
    pip install pytest requests
    ```
3.  **Ligue o Mockoon:** Abra o Mockoon, inicie o `Banco Externo Stone` (botão **Play** verde).
4.  **Execute os Testes:**
    ```bash
    pytest tests -v
    ```
    *Resultado Esperado:* 3 testes aprovados.


