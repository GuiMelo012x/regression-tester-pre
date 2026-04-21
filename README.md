# Regression Tester: Avaliação de LLMs em Testes de Regressão

O objetivo deste trabalho é avaliar a eficácia de diferentes LLMs (Gemini, Cohere e Llama 3) na identificação de testes de regressão impactados através da análise de ficheiros `git diff`.

## 🧪 Metodologia

A pesquisa utiliza um dataset de **30 amostras** de código Java, balanceado entre mudanças que exigem novos testes e refatorações benignas:

- **Casos com Erro (Gabarito: Teste Específico):** Injeção de falhas lógicas, como erros de concorrência (`amostra-18.diff`), falhas de imutabilidade de Strings (`amostra-23.diff`) e erros de iteração de coleções (`amostra-24.diff`).
- **Casos de Refatoração (Gabarito: Nenhum):** Mudanças de estilo e sintaxe que não alteram o comportamento, como adoção de `var` (`amostra-25.diff`) ou adição de anotações `@Override` (`amostra-26.diff`).

## 📂 Estrutura do Repositório

- `amostras/`: Contém os 30 ficheiros `.diff` utilizados como input para os modelos.
- `reg.py`: Script principal que automatiza as chamadas às APIs e consolida os resultados.
- `requirements.txt`: Lista de dependências necessárias para a execução do projeto.
- `Gabarito - A SER ADICIONADO`: A base de referência (ground truth) para o cálculo das métricas de precisão.
