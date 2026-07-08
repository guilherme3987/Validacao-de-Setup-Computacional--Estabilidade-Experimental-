# Engenharia de Programas — Análise de Algoritmos

Repositório da disciplina **Engenharia de Programas**, contendo estudos experimentais e teóricos sobre complexidade de algoritmos de ordenação.

---

## Estrutura do Repositório

### `av1/` — Validação de Setup Computacional

**Objetivo:** Verificar se o ambiente de execução (hardware + SO) é estatisticamente estável para realizar medições confiáveis.

- Gera listas aleatórias de tamanhos N = {100, 500, 1000, 2000, 3000}
- Executa `sorted()` nativo do Python por 30 repetições em 3 períodos distintos (T1, T2, T3)
- Calcula o **Coeficiente de Variação (CV = σ/μ)** — critério de aprovação: CV ≤ 0.15 (15%)
- Gera boxplots, histogramas com KDE e gráfico de barras do CV

**Arquivos:**
- `validacao_setup.py` — script principal de coleta e plotagem
- `resultados/` — gráficos gerados (boxplot+histograma, CV)
- `README.MD` — documentação detalhada

---

### `av2/` — Análise Empírica de Complexidade (Tempo)

**Objetivo:** Determinar empiricamente a classe de complexidade assintótica do Quicksort e Shell Sort medindo **tempo real de execução** e ajustando modelos de regressão não-linear.

- Algoritmos: Quicksort iterativo (pivô mediana-de-três) e Shell Sort (sequência de Ciura)
- Mede tempo de execução para N = {2k, 8k, 20k, 50k, 100k}
- Ajusta 5 modelos (O(log n), O(n), O(n log n), O(n²), O(n³)) via `scipy.optimize.curve_fit`
- Seleciona o melhor modelo pelo maior R²

**Resultados obtidos:**
| Algoritmo | Melhor modelo | R² |
|:----------|:-------------:|---:|
| Quicksort | O(n log n) | 0.9998 |
| Shell Sort | O(n²) | 0.9943 |

**Arquivos:**
- `sorting.py` — implementação dos algoritmos
- `benchmarking.py` — coleta de tempos com protocolo de dupla validação
- `models.py` — funções de ajuste de curva
- `visualization.py` — plotagem dos gráficos
- `main.py` — script principal
- `resultados/imagens/` — gráficos gerados

---

### `av3/` — Fundamentos Teóricos: Indução, Expansão Telescópica e F.O.C.A.

**Objetivo:** Apresentação dos conceitos matemáticos e do paradigma F.O.C.A. para contagem de operações primitivas em algoritmos.

- **Indução Completa:** Demonstração da soma dos n primeiros naturais
- **Expansão Telescópica:** Resolução de recorrências lineares pelo cancelamento de termos
- **Paradigma F.O.C.A.:** Contagem de Funções, Operações aritméticas, Comparações e Atribuições
- Exemplo prático: análise completa da multiplicação de matrizes (custo O(n³))

**Arquivos:**
- `Untitled-1.` — slides em formato Marp (Markdown Presentation)
- `Relatório_de_Avaliação_Experimental_de_Complexidade.pdf` — relatório em PDF

---

### `av4/` — Análise de Operações Totais vs N

**Objetivo:** Contar o **número total de operações elementares** (comparações + trocas/atribuições) realizadas pelo Quicksort e Shell Sort em função de N, eliminando o ruído do ambiente.

- Versões instrumentadas: `quicksort_ops()` e `shell_sort_ops()` que retornam a contagem de operações
- Também mede **tempo real** para comparar as curvas normalizadas
- Gera 3 gráficos: operações vs N, comparação normalizada para cada algoritmo

**Resultados obtidos (N = 100k):**
| Algoritmo | Operações | Tempo |
|:----------|----------:|------:|
| Quicksort | 2.937.978 | 135.922 μs |
| Shell Sort | 18.660.359 | 675.796 μs |

As curvas normalizadas de operações e tempo praticamente se sobrepõem, validando que a contagem de operações é um preditor fiel do tempo real.

**Arquivos:**
- `sorting.py` — algoritmos + versões com contagem de operações
- `main.py` — script principal (coleta e plotagem)
- `visualization.py` — funções de plotagem (3 gráficos)
- `resultados/imagens/` — gráficos gerados
- `README.MD` — documentação com código comentado e gráficos

---

## Dependências

```bash
pip install numpy scipy matplotlib pandas seaborn
```

---

## Licença

Projeto acadêmico — disciplina de Engenharia de Programas.
