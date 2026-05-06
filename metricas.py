import pandas as pd
import re

# Etapa 1 - Carregar os dados
print("Carregando os dados...")
df_resultados = pd.read_csv('resultados_tcc.csv')
df_gabarito = pd.read_csv('Gabarito.csv', sep=';') # O gabarito usa ponto e vírgula

# Etapa 2 - Alinha os ficheiros através do número da amostra, como amostra-1.diff, amostra-2.diff, etc.
df_resultados['Amostra'] = df_resultados['Arquivo'].apply(lambda x: int(re.findall(r'\d+', x)[0]))
df_completo = pd.merge(df_resultados, df_gabarito, on='Amostra')
modelos = ['Gemini', 'Cohere', 'Llama3']
metricas = {}

total_tentativas = len(df_completo) # Conta exatamente quantas amostras o script processou (ex: 30)
print(f"Total de Amostras (Tentativas) processadas: {total_tentativas}\n")
print("Calculando as métricas...\n")

for modelo in modelos:
    vp = 0 # Verdadeiro Positivo: Tinha erro e a IA achou
    vn = 0 # Verdadeiro Negativo: NÃO tinha erro (Nenhum) e a IA disse "Nenhum"
    fp = 0 # Falso Positivo: NÃO tinha erro, mas a IA inventou um teste
    fn = 0 # Falso Negativo: Tinha erro e a IA ignorou (ou deu erro de API)

    for index, row in df_completo.iterrows():
        gabarito_original = str(row['Gabarito']).strip().lower()
        resposta_modelo = str(row[modelo]).strip().lower()

        if resposta_modelo == 'erro': # Se o modelo não conseguiu gerar uma resposta, consideramos isso como um erro falha grave, ou seja, um FN
            fn += 1 
            continue

        if gabarito_original == 'nenhum':
            # Cenário 1 - Refatoração Benigna
            if 'nenhum' in resposta_modelo:
                vn += 1 # O modelo acertou que não tinha teste impactado
            else:
                fp += 1 # O modelo inventou um teste onde não tinha

        else:
            # Cenário 2 - Injeção de Falha
            termo_chave = gabarito_original.replace('test', '').strip()
            if termo_chave in resposta_modelo:
                vp += 1 # O modelo acertou que tinha o teste impactado
            else:
                fn += 1 # O modelo falhou em identificar o teste impactado


    # --- CÁLCULO DAS FÓRMULAS ---
    taxa_acerto = ((vp + vn) / total_tentativas) * 100 if total_tentativas > 0 else 0 # Taxa de Acerto (Acurácia): Todos os acertos (VP + VN) divididos pelo Total
    precisao = vp / (vp + fp) if (vp + fp) > 0 else 0 # Precisão: Dos casos que o modelo disse que tinha teste impactado (VP + FP), quantos ele acertou (VP)
    recall = vp / (vp + fn) if (vp + fn) > 0 else 0 # Recall: Dos casos que realmente tinham teste impactado (VP + FN), quantos o modelo conseguiu identificar (VP)
    f1 = 2 * (precisao * recall) / (precisao + recall) if (precisao + recall) > 0 else 0 # F1-Score: A média harmônica entre Precisão e Recall, para balancear os dois aspectos
    
    metricas[modelo] = {
        'Tentativas': total_tentativas,
        'Taxa de Acerto': taxa_acerto,
        'Precisão': precisao * 100,
        'Recall': recall * 100,
        'F1-Score': f1 * 100,
        'VP': vp, 'VN': vn, 'FP': fp, 'FN': fn
    }