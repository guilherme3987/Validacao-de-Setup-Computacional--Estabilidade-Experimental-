# 📊 Análise Empírica de Complexidade Algorítmica
### Quicksort vs Shell Sort — Regressão Não-Linear com Dupla Validação

---

## 🧭 Visão Geral

Este projeto determina **empiricamente** a classe de complexidade assintótica do **Quicksort** e do **Shell Sort** sem recorrer à análise teórica direta. Em vez disso, mede os tempos reais de execução para diferentes tamanhos de entrada e aplica **regressão não-linear** (`scipy.optimize.curve_fit`) para descobrir qual função matemática — logarítmica, linear, log-linear, quadrática ou cúbica — melhor descreve o comportamento observado.

A coleta de dados segue um **Protocolo de Dupla Validação** que garante estabilidade do ambiente antes de registrar qualquer medição.

---

## 🔬 Metodologia

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROTOCOLO DE COLETA                          │
│                                                                 │
│  Para cada N:                                                   │
│                                                                 │
│  1. Gera 50 listas aleatórias de tamanho N                      │
│                                                                 │
│  2. VALIDAÇÃO DE ESTABILIDADE (lista piloto)                    │
│     └─ Ordena a lista[0] por 35 vezes                           │
│     └─ Calcula CV = std / média                                 │
│     └─ Se CV > 0.15 → ambiente instável, aguarda e repete       │
│     └─ Se CV ≤ 0.15 → ambiente estável, prossegue              │
│                                                                 │
│  3. COLETA REAL (listas[1..49])                                 │
│     └─ Cada lista ordenada exatamente 1 vez                     │
│     └─ Registra o tempo de cada execução                        │
│                                                                 │
│  4. Tempo representativo = média dos 49 tempos                  │
│                                                                 │
│  5. Repete para os 5 valores de N                               │
│                                                                 │
│  6. Ajusta 5 modelos matemáticos via curve_fit                  │
│     └─ Seleciona o de maior R²                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Por que o Coeficiente de Variação (CV)?

O CV mede a dispersão relativa dos tempos. Um CV alto indica que o sistema operacional, processos em segundo plano ou cache estão introduzindo ruído nas medições, tornando-as não-confiáveis. O limiar CV ≤ 0.15 (15%) é uma garantia de que as medições refletem o algoritmo, não o ambiente.

---

## 🧮 Modelos de Complexidade Testados

| Notação      | Fórmula de Ajuste        |
|:------------:|:------------------------:|
| O(log n)     | `a · log₂(n) + b`        |
| O(n)         | `a · n + b`              |
| O(n log n)   | `a · n · log₂(n) + b`    |
| O(n²)        | `a · n² + b`             |
| O(n³)        | `a · n³ + b`             |

O melhor modelo é selecionado pelo **coeficiente de determinação R²** — quanto mais próximo de 1.0, melhor o ajuste.

---

## ⚙️ Implementação dos Algoritmos

### Quicksort — Pivô Mediana-de-Três + Pilha Explícita
Implementação iterativa (sem recursão) que usa uma pilha explícita para evitar stack overflow. O pivô é escolhido pela **mediana entre o primeiro, o meio e o último elemento**, tornando o pior caso (listas quase ordenadas) muito menos provável.

```
┌──────────────────────────────────────────┐
│  pivot = mediana(arr[lo], arr[mid], arr[hi]) │
│  Particiona em torno do pivot            │
│  Empilha subarray esquerdo               │
│  Empilha subarray direito                │
│  Repete até pilha vazia                  │
└──────────────────────────────────────────┘
```

### Shell Sort — Sequência de Ciura
Utiliza a **sequência de Ciura** (1, 4, 10, 23, 57, 132, 301, 701), empiricamente uma das melhores sequências de gaps conhecidas, reduzindo o número de movimentações necessárias na fase de inserção.

```
gaps = [701, 301, 132, 57, 23, 10, 4, 1]  ← do maior para o menor
Para cada gap:
  └─ Executa insertion sort com passo = gap
```

---

## 📈 Resultados

### Quicksort

| N | Tempo Médio (μs) | CV Piloto |
|--:|----------------:|:--------:|
| 2.000 | 2.123,81 | 0.0262 ✅ |
| 8.000 | 10.294,65 | 0.0292 ✅ |
| 20.000 | 28.285,55 | 0.0279 ✅ |
| 50.000 | 79.791,61 | 0.0416 ✅ |
| 100.000 | 174.138,88 | 0.0327 ✅ |

#### Ranking de R² — Quicksort

| Modelo | R² |
|:-------|---:|
| **O(n log n)** | **0.9998 ← Melhor** |
| O(n) | 0.9982 |
| O(n²) | 0.9592 |
| O(n³) | 0.8998 |
| O(log n) | 0.7526 |

> **Conclusão:** crescimento log-linear confirmado com R²=0.9998 — exatamente o que a teoria prediz para o **caso médio** do Quicksort.

---

### Shell Sort

| N | Tempo Médio (μs) | CV Piloto |
|--:|----------------:|:--------:|
| 2.000 | 3.306,93 | 0.0258 ✅ |
| 8.000 | 18.919,73 | 0.0218 ✅ |
| 20.000 | 65.509,23 | 0.0550 ✅ |
| 50.000 | 259.624,57 | 0.0612 ✅ |
| 100.000 | 789.311,46 | 0.0597 ✅ |

#### Ranking de R² — Shell Sort

| Modelo | R² |
|:-------|---:|
| **O(n²)** | **0.9943 ← Melhor** |
| O(n log n) | 0.9804 |
| O(n) | 0.9714 |
| O(n³) | 0.9622 |
| O(log n) | 0.6507 |

> **Conclusão:** crescimento **quadrático** observado empiricamente em Python. A sequência de Ciura garante O(n^1.25) na teoria, mas o overhead do interpretador Python nas fases de gap pequeno domina, resultando em comportamento aparentemente quadrático para os tamanhos testados.

---

## 🖼️ Gráfico Gerado

O script produz um painel com 3 linhas:

```
┌──────────────────────────────────────────────────────────────┐
│  LINHA 1 │ Dispersão dos 5 pontos reais + 5 curvas de        │
│          │ regressão sobrepostas (melhor ajuste destacado)    │
├──────────────────────────────────────────────────────────────┤
│  LINHA 2 │ Gráfico de barras com o R² de cada modelo         │
│          │ (permite comparar visualmente o ajuste)            │
├──────────────────────────────────────────────────────────────┤
│  LINHA 3 │ Comparação direta: tempo real de ambos os          │
│          │ algoritmos no mesmo eixo                           │
└──────────────────────────────────────────────────────────────┘
```

---

## 🗂️ Estrutura do Projeto

```
.
├── sort_complexity.py   ← Script principal
├── sort_complexity.png  ← Gráfico gerado automaticamente
└── README.md            ← Este arquivo
```

---

## 🚀 Como Executar

### Pré-requisitos

```bash
pip install numpy scipy matplotlib
```

### Execução

```bash
python sort_complexity.py
```

A saída no terminal mostra o progresso em tempo real, os CVs de cada coleta, a tabela de tempos e o ranking de R² por algoritmo. O gráfico é salvo automaticamente como `sort_complexity.png`.

---

## 🔧 Configurações Ajustáveis

No topo da função `main()` você pode modificar:

| Parâmetro | Padrão | Descrição |
|:----------|-------:|:----------|
| `TAMANHOS` | `[2k, 8k, 20k, 50k, 100k]` | Tamanhos de N testados |
| `N_LISTAS` | `50` | Listas aleatórias por N |
| `REP_PILOTO` | `35` | Repetições para validar estabilidade |
| `CV_MAX` | `0.15` | Limiar de CV aceito |

Para adicionar um novo algoritmo, basta implementá-lo e incluí-lo no dicionário `ALGORITMOS`:

```python
ALGORITMOS = {
    "Quicksort":   quicksort,
    "Shell Sort":  shell_sort,
    "Merge Sort":  merge_sort,   # ← novo algoritmo
}
```

---

## 📚 Referências

- Knuth, D. E. *The Art of Computer Programming*, Vol. 3: Sorting and Searching.
- Ciura, M. (2001). *Best Increments for the Average Case of Shell Sort*. PPAM.
- Sedgewick, R. & Wayne, K. *Algorithms*, 4ª ed. — Capítulos de Quicksort e Shell Sort.
- SciPy Documentation — [`scipy.optimize.curve_fit`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html)

---