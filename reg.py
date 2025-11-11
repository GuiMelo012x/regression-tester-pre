import google.generativeai as genai # pip install google-generativeai

api_key = "AIzaSyBA5S_3VZRCkOmdzXFN3nMY-15_hHADQ6I"
genai.configure(api_key=api_key)

print("Conectando com o Gemini")

model = genai.GenerativeModel('gemini-pro')

response = model.generate_content("Qual a capital de Pernambuco?") # Teste

print("Conexão realizada")

print("\nResposta do Gemini:")
print(response.txt)
