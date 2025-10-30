# tests/test_transactions.py

import pytest   # A biblioteca de testes (framework)
import requests # A biblioteca que faz as chamadas de API (o "curl" do Python)
from config import BASE_URL # Importa a URL do nosso config

# --- DADOS DE TESTE ---
# Estes são os dados que enviamos para a API (o "payload")
TRANSACTION_PAYLOAD = {
    "amount": 100.50,
    "card_number": "4111222233334444",
    "cvv": "123"
}

# --- CENÁRIO 1: O CAMINHO FELIZ (HAPPY PATH) ---
def test_transaction_approved_success():
    """
    [Cenário 1: Sucesso]
    Valida o fluxo de sucesso (Happy Path).
    Verifica se a API responde 200 (OK) e se o JSON de resposta
    contém o status 'APPROVED'.
    
    Argumento (Nível Pleno): Garante a funcionalidade básica da API.
    """
    print("\n[TESTE 1] Rodando: Happy Path (/authorize/success)")
    
    # 1. Preparação: Define a URL alvo (Rota 1 do Mockoon)
    url = f"{BASE_URL}/authorize/success"
    
    # 2. Execução: Faz a chamada POST para o Mockoon
    response = requests.post(url, json=TRANSACTION_PAYLOAD)
    
    # 3. Verificação (Asserts):
    
    # Verifica se o código HTTP foi 200 (OK)
    assert response.status_code == 200, "Falha: O Status Code deveria ser 200"
    
    # Converte a resposta de texto para JSON (um dicionário Python)
    data = response.json()
    
    # Verifica o CONTEÚDO da resposta
    assert data["status"] == "APPROVED", "Falha: O status no JSON não é 'APPROVED'"
    assert "transaction_id" in data, "Falha: O campo 'transaction_id' está faltando na resposta"
    
    print("[TESTE 1] PASSOU: Happy Path validado.")


# --- CENÁRIO 2: RESILIÊNCIA (TIMEOUT / SINAL RUIM DO POS) ---
def test_transaction_handles_bank_timeout():
    """
    [Cenário 2: Resiliência - Nível Engineer III]
    Valida a Resiliência do sistema (o foco do projeto).
    O Mock (Banco) está configurado para demorar 10 segundos.
    Nosso sistema (o teste) deve desistir em 5 segundos (timeout=5).
    
    Argumento (Hardware + QA III): Isso simula a falha de sinal do POS na rua.
    Se o teste falhar por 'Timeout', é um SUCESSO de resiliência.
    """
    print("\n[TESTE 2] Rodando: Resiliência/Timeout (/authorize/timeout)... (vai demorar 5s)")
    
    # 1. Preparação: Define a URL alvo (Rota 2 do Mockoon)
    url = f"{BASE_URL}/authorize/timeout"
    
    # 2. Execução e Verificação (Asserts):
    # Usamos 'pytest.raises' para verificar se a exceção 'Timeout' ACONTECE.
    with pytest.raises(requests.exceptions.Timeout):
        
        # O sistema Stone (nosso 'requests') não pode esperar os 10s do banco.
        # Ele DEVE falhar em 5 segundos.
        response = requests.post(
            url, 
            json=TRANSACTION_PAYLOAD, 
            timeout=5 # Este é o timeout do NOSSO sistema (Resiliência)
        )

    # 3. Conclusão:
    # Se o código chegou até aqui, significa que o 'pytest.raises' capturou
    # a exceção de Timeout com sucesso.
    print("[TESTE 2] PASSOU: O sistema foi resiliente e falhou por timeout em 5s (Comportamento Esperado).")


# --- CENÁRIO 3: ERRO DE CONTRATO (API DO BANCO MUDOU) ---
def test_transaction_handles_contract_error():
    """
    [Cenário 3: Contrato - Nível Engineer III]
    Valida a Quebra de Contrato.
    O Mock (Banco) está retornando um JSON com campos errados ("estado" em vez de "status").
    Nosso sistema deve detectar essa quebra.
    
    Argumento (Visão de Arquiteto): Prova a necessidade de Testes de Contrato (PactFlow).
    """
    print("\n[TESTE 3] Rodando: Quebra de Contrato (/authorize/contract-error)")
    
    # 1. Preparação: Define a URL alvo (Rota 3 do Mockoon)
    url = f"{BASE_URL}/authorize/contract-error"
    
    # 2. Execução:
    response = requests.post(url, json=TRANSACTION_PAYLOAD)
    
    # 3. Verificação (Asserts):
    
    # A chamada HTTP funcionou, o banco respondeu 200 OK
    assert response.status_code == 200, "Falha: O Status Code deveria ser 200"
    
    # Pegamos o JSON quebrado ({"estado": "APROVADO", ...})
    data = response.json()
    
    # Agora, validamos o CONTRATO.
    # Usamos um 'try/except' para verificar se o campo esperado existe.
    try:
        # Nosso sistema espera o campo "status"
        status = data["status"]
        
        # Se o código chegar aqui, o campo "status" EXISTE, o que está errado!
        pytest.fail("FALHA DE CONTRATO: O teste esperava um erro (KeyError) mas o campo 'status' foi encontrado.")
        
    except KeyError:
        # Se o código cair aqui (KeyError), é um SUCESSO!
        # O campo 'status' não foi encontrado (o Mock mandou 'estado').
        assert True
        print("[TESTE 3] PASSOU: Quebra de contrato detectada (Campo 'status' não encontrado).")