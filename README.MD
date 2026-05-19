Aqui está uma proposta de README unificado, consolidando as duas fases do seu projeto de forma lógica e profissional.

---

# 📊 Projeto de Engenharia de Programas: Validação de Setup e Análise Empírica de Complexidade

Este repositório consolida um estudo rigoroso em duas etapas para a disciplina de Engenharia de Programas. O objetivo geral é estabelecer um ambiente computacional estatisticamente estável e, a partir dele, determinar empiricamente a classe de complexidade assintótica de algoritmos de ordenação por meio de regressão não-linear.

O projeto é dividido em duas fases principais:

1. **AV1 - Validação de Setup Computacional:** Garantia de estabilidade experimental.
2. **AV2 - Análise de Complexidade Empírica:** Quicksort vs Shell Sort.

---

## 🧭 Visão Geral das Fases

### 🔹 Fase 1: Validação do Setup (Estabilidade Experimental)

Antes de testar o desempenho dos algoritmos, é essencial garantir que o hardware e o sistema operacional não introduzam ruído nas medições.

* **Objetivo:** Medir tempos de execução básicos e avaliar a estabilidade ao longo de 3 períodos temporais (T1, T2, T3) para mitigar anomalias.
* **Métrica-Chave (CV):** Utilizamos o Coeficiente de Variação ($CV = \sigma/\mu$). O critério mestre de aprovação exige que $CV \le 0.15$ (15%). Valores acima disso indicam interferência no ambiente (processos em background, cache, etc.), reprovando o setup.
* **Carga de Trabalho:** Listas de tamanho $N \in \{100, 500, 1000, 2000, 3000\}$ com 30 repetições cada.

### 🔹 Fase 2: Análise Empírica (Quicksort vs Shell Sort)

Com o ambiente validado, aplicamos um **Protocolo de Dupla Validação** para medir tempos reais de ordenação e descobrir a classe de complexidade sem recorrer à análise teórica direta.

* **Algoritmos Testados:** * **Quicksort:** Implementação iterativa com pilha explícita e pivô mediana-de-três.
* **Shell Sort:** Implementação com a sequência de gaps de Ciura (1, 4, 10, 23, 57...).


* **Regressão Não-Linear:** Uso do `scipy.optimize.curve_fit` para testar os tempos reais contra 5 modelos matemáticos: $O(\log n)$, $O(n)$, $O(n \log n)$, $O(n^2)$ e $O(n^3)$. O modelo com o $R^2$ (coeficiente de determinação) mais próximo de 1.0 é declarado o vencedor.
* **Carga de Trabalho:** Listas de tamanho $N$ variando de 2.000 a 100.000, com 50 listas geradas por tamanho.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* **NumPy & Pandas:** Manipulação de matrizes, estruturação de dados e cálculos estatísticos.
* **SciPy:** Ajuste assintótico de curvas e regressão não-linear (`curve_fit`).
* **Matplotlib & Seaborn:** Geração de gráficos, boxplots, histogramas e curvas de dispersão.

---

## 📈 Resumo dos Resultados

* **Validação do Ambiente (AV1):** O setup deve ser aprovado em todos os tamanhos de $N$ e ciclos temporais para garantir que o ruído do sistema não contamine a AV2.
* **Resultados Quicksort (AV2):** O algoritmo comprovou empiricamente um crescimento log-linear ($O(n \log n)$), atingindo um $R^2 = 0.9998$, confirmando seu caso médio teórico robusto com a mediana-de-três.
* **Resultados Shell Sort (AV2):** O algoritmo apresentou comportamento que se aproximou de $O(n^2)$ com $R^2 = 0.9943$. Embora a sequência de Ciura garanta performance teórica superior ($O(n^{1.25})$), o overhead do interpretador Python nas fases de *gap* pequeno acaba dominando os tempos medidos para os valores de $N$ testados.

---

## 🚀 Como Configurar e Executar

**1. Instale as dependências:**
Abra o terminal e execute:

```bash
pip install numpy pandas scipy matplotlib seaborn

```

**2. Isole o Ambiente:**
Antes de executar qualquer teste, recomenda-se fechar navegadores, desconectar a internet (se possível) e encerrar aplicações pesadas em segundo plano para garantir o rigor do Coeficiente de Variação ($CV \le 15\%$).

**3. Execução:**
Para rodar a validação de setup (Fase 1):

```bash
python validacao_setup.py

```

Para rodar a análise de algoritmos (Fase 2) usando a nova arquitetura modular:

```bash
cd resultados
python main.py

```

---

## 🗂️ Artefatos Visuais Gerados

O projeto gera automaticamente uma pasta de `resultados/` com diversos artefatos visuais:

* `5_1_5_2_boxplot_histograma.png`: Grade com boxplots e curvas KDE mostrando a dispersão dos tempos base.
* `5_3_cv_barras.png`: Gráfico consolidado do Coeficiente de Variação com o limiar de 15%.
* `sort_complexity.png` (ou os painéis separados de dispersão): Gráficos plotando os pontos reais de tempo de execução sobrepostos às 5 curvas matemáticas ajustadas para cada algoritmo.

---

*Projeto desenvolvido para a disciplina de Engenharia de Programas.*