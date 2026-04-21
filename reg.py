import google.generativeai as genai # pip install google-generativeai
import cohere # pip install cohere
import requests 
import re
import os
import glob
import time
import pandas as pd
from dotenv import load_dotenv # pip install python-dotenv


load_dotenv() # Carrega variáveis de ambiente do arquivo .env"
google_api_key = os.getenv("GOOGLE_API_KEY") # Pega a chave do Google
cohere_api_key = os.getenv("COHERE_API_KEY") # Pega a chave do Cohere
hf_api_key = os.getenv("HF_API_KEY") # Pega a chave do Hugging Face

if not google_api_key or not cohere_api_key or not hf_api_key:
    print("Erro: Chaves de API não encontradas no .env")
    print("Verifique seu .env")
    exit() # Para o programa se as chaves não forem encontradas

# Configuração das APIs
genai.configure(api_key=google_api_key) # Configura a chave da API do Google
co_client = cohere.Client(cohere_api_key) # Configura a chave da API do Cohere
hf_headers = {"Authorization": f"Bearer {hf_api_key}"} # Cabeçalho de autorização

# --- Prompt Mestre ---
# Deve dizer quem a IA é, o que fazer com o arquivo .diff e o que ela deve responder.

MASTER_PROMPT_TEMPLATE = """
Você é um engenheiro de QA Sênior especialista em testes de regressão.
Você deve analisar o 'git diff' de uma mudança de código e identificar quais testes existentes precisam ser executados para validar essa mudança.

Responda APENAS com uma lista dos nomes dos testes impactados, separados por vírgula.
Se nenhum teste for impactado, responda "Nenhum".

Git Diff:
---
{diff_content}
---
Testes impactados:
"""

# ---------- IAs ----------

# Criação da lista vazia antes do loop para guardar os resultados
resultados = []

# --- INÍCIO DO ÚNICO LOOP DE ARQUIVOS ---
ficheiros = sorted(glob.glob("amostras/*.diff"), key=lambda x: int(re.findall(r'\d+', x)[0]))
for filepath in ficheiros:
    print(f"\n======== PROCESSANDO: {filepath} ========")
    
    with open(filepath, "r", encoding="utf-8") as file:
        diff_text = file.read()

    # O prompt é gerado AQUI DENTRO, pois a variável diff_text já tem o conteúdo lido
    final_prompt = MASTER_PROMPT_TEMPLATE.format(diff_content=diff_text)
    
    # Variáveis padrão para guardar as respostas desta iteração
    resp_gemini = "Erro"
    resp_cohere = "Erro"
    resp_hf = "Erro"

    # ---------- Gemini ----------
    try:
        print("Conectando com o Gemini...")
        model_gemini = genai.GenerativeModel("gemini-1.5-flash")
        response_gemini = model_gemini.generate_content(final_prompt) 
        resp_gemini = response_gemini.text.strip()
        print("Resposta do Gemini:", resp_gemini)
    except Exception as e:
        print("Erro ao conectar com o Gemini:", str(e))

    # ---------- Cohere ----------
    try:
        print("Conectando com o Cohere...")
        response_cohere = co_client.chat(
            model='command-a-03-2025',
            message=final_prompt 
        )
        resp_cohere = response_cohere.text.strip()
        print("Resposta do Cohere:", resp_cohere)
    except Exception as e:
        print("Erro ao conectar com o Cohere:", str(e))

    # ---------- Hugging Face (Llama 3) ----------
    API_URL = "https://router.huggingface.co/v1/chat/completions"
    payload = {
        "model": "meta-llama/Meta-Llama-3-8B-Instruct",
        "messages": [{"role": "user", "content": final_prompt}], 
        "max_tokens": 256,
        "temperature": 0.0
    }

    try:
        print("Conectando com o Hugging Face...")
        response_hf = requests.post(API_URL, headers=hf_headers, json=payload)
        response_hf.raise_for_status() 
        result = response_hf.json()
        resp_hf = result['choices'][0]['message']['content'].strip()
        print("Resposta do Llama 3:", resp_hf)
    except Exception as e:
        print(f"Erro ao conectar com o Hugging Face: {e}")
        
    # Guarda os dados desta amostra na lista de resultados
    resultados.append({
        "Arquivo": os.path.basename(filepath),
        "Gemini": resp_gemini,
        "Cohere": resp_cohere,
        "Llama3": resp_hf
    })
    # A pausa obrigatória para respeitar a Free Tier, pois estava bloqueando por "muitas requisições".
    print("Aguardando 5 segundos para evitar bloqueios de API...") 
    time.sleep(5)

# --- FIM DO LOOP ---

# 3. Uso do Pandas para transformar a lista de dicionários num CSV
print("\nGerando arquivo resultados_tcc.csv...")
df = pd.DataFrame(resultados)
df.to_csv("resultados_tcc.csv", index=False, encoding="utf-8")
print("Sucesso! Resultados salvos em 'resultados_tcc.csv'. Pode abrir no Excel!")