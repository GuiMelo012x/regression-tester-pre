import google.generativeai as genai # pip install google-generativeai
import cohere # pip install cohere
import os
from dotenv import load_dotenv # pip install python-dotenv

load_dotenv() # Carrega variáveis de ambiente do arquivo .env"
google_api_key = os.getenv("GOOGLE_API_KEY") # Pega a chave do Google
cohere_api_key = os.getenv("COHERE_API_KEY") # Pega a chave do Cohere

if not google_api_key or not cohere_api_key:
    print("Erro: Chaves de API não encontradas no arquivo .env,")
    print("Verifique se as keys estão no seu .env")
    exit() # Para o script se não achar as chaves

genai.configure(api_key=google_api_key) # Configura a chave da API do Google
co_client = cohere.Client(cohere_api_key) # Configura a chave da API do Cohere

# --- Pergunta de Teste ---
pergunta = "Qual a capital de Pernambuco?"
print(f"Pergunta: {pergunta}\n")

    # ---------- Testando o Gemini ----------
try:
    print("---------- Gemini ----------")
    print("Conectando com o Gemini...")
    model_gemini = genai.GenerativeModel("gemini-2.5-pro")
    response_gemini = model_gemini.generate_content(pergunta)
    print("Resposta do Gemini:", response_gemini.text)
except Exception as e:
    print("Erro ao conectar com o Gemini:", str(e))


     # ---------- Testando o Cohere ----------
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