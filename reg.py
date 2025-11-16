import google.generativeai as genai # pip install google-generativeai
import cohere # pip install cohere
import requests 
import os
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

# --- Ler o arquivo DIFF ---
try:
    with open("amostras/amostra-1.diff","r", encoding="utf-8") as file:
        diff_text = file.read()
        print("Arquivo 'amostra-1.diff' lido com sucesso.")
except FileNotFoundError:
    print("Arquivo 'amostra-1.diff' não encontrado.")
    exit()

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


# O Python pega o texto do arquivo diff e insere no lugar de {diff_content} dentro do template do prompt.
final_prompt = MASTER_PROMPT_TEMPLATE.format(diff_content=diff_text) 

print("\n--- PROMPT CRIADO COM SUCESSO ---")
print(final_prompt)
print("---------------------------------\n")
 


"""
# ---------- IAs ----------



# ---------- Gemini ----------
try:
    print("---------- Gemini ----------")
    print("Conectando com o Gemini...")
    model_gemini = genai.GenerativeModel("gemini-2.5-pro")
    response_gemini = model_gemini.generate_content(pergunta)
    print("Resposta do Gemini:", response_gemini.text)
except Exception as e:
    print("Erro ao conectar com o Gemini:", str(e))


# ---------- Cohere ----------
print("\n---------- Cohere ----------")

try:
    print("Conectando com o Cohere...")
    response_cohere = co_client.chat (
        model='command-a-03-2025',
        message=pergunta
    )
    print("Resposta do Cohere:", response_cohere.text)
except Exception as e:
    print("Erro ao conectar com o Cohere:", str(e))

# ---------- Hugging Face (Llama 3) ----------
print("\n---------- Hugging Face (Llama 3) ----------")

API_URL = "https://router.huggingface.co/v1/chat/completions"

payload = {
    "model": "meta-llama/Meta-Llama-3-8B-Instruct",
    "messages": [{"role": "user", "content": pergunta}],
    "max_tokens": 256,
    "temperature": 0.7
}

try:
    print("Conectando com o Hugging Face...")
    response_hf = requests.post(API_URL, headers=hf_headers, json=payload)
    
    # Vai pra exceção se houver qualquer erro de API
    response_hf.raise_for_status() 
    
    result = response_hf.json()
    print("Resposta do Llama 3:", result['choices'][0]['message']['content'])

except Exception as e:
    # Captura erros (ex: falhas de rede, JSON inválido)
    print(f"Erro inesperado ao conectar com o Hugging Face: {e}")
"""