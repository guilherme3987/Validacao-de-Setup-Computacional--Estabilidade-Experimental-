# Validação de Setup Computacional (Estabilidade Experimental)

Este projeto contém o script de automação e análise estatística para validar a estabilidade de um ambiente computacional (Hardware, Sistema Operacional e IDE). O objetivo é garantir que o setup possui baixo nível de ruído e é estatisticamente confiável para a realização de medições empíricas de complexidade de algoritmos.

## 🎯 Objetivos de Aprendizagem
* Desenvolver um script em Python para medir tempos de execução de operações computacionais.
* Realizar coleta e análise estatística de dados para avaliar a estabilidade experimental.
* Executar testes em diferentes períodos temporais para identificar possíveis interferências de processos em segundo plano do Sistema Operacional.
* Calcular e interpretar o Coeficiente de Variação ($CV = \sigma/\mu$) para verificar a confiabilidade do setup.
* Gerar visualizações avançadas (boxplots, histogramas e gráficos de barras) para a composição do relatório técnico.

## ⚙️ Metodologia e Critérios de Aceite
A rotina de validação segue rigorosamente os seguintes parâmetros:
* **Carga de Trabalho:** Testes em listas de tamanhos $n \in \{100, 500, 1000, 2000, 3000\}$.
* **Amostragem:** Realização de **30** repetições para cada tamanho de $n$.
* **Resiliência Temporal:** Execução distribuída em **3** períodos distintos (**T1, T2, T3**) para mitigar anomalias temporárias de hardware/software.
* **Critério Mestre de Aprovação:** O Coeficiente de Variação de cada bateria de testes deve ser estritamente $CV \le 0.15$ (ou **15%**). Caso o limite seja ultrapassado, o setup é considerado **Reprovado** e exige o isolamento de processos em background antes de uma nova tentativa.

## 🛠️ Tecnologias Utilizadas
* **Python 3.x**
* **Pandas & Numpy:** Estruturação e cálculos estatísticos.
* **Matplotlib & Seaborn:** Plotagem dos gráficos de validação.

## 🚀 Como Executar

**1. Instale as dependências necessárias:**
Abra o terminal e execute:
```bash
pip install numpy pandas matplotlib seaborn
```

**2. Isole o ambiente:**
Antes de executar, é estritamente recomendado fechar navegadores, desconectar a internet (Wi-Fi) e encerrar processos pesados em segundo plano para evitar "ruído" nos testes.

**3. Rode o script:**
```bash
python validacao_setup.py
```

## 📊 Estrutura de Resultados
Ao finalizar a execução, o script imprimirá uma **Tabela de Validação** diretamente no terminal, detalhando o CV de cada período e o status de aprovação.

Além disso, uma pasta chamada `resultados/` será criada automaticamente no diretório do script, contendo os artefatos visuais exigidos para o relatório:

1. **`5_1_5_2_boxplot_histograma.png`**: Figura unificada em grade $2 \times 5$ com boxplots (linha superior) e histogramas com curva de densidade KDE (linha inferior) para cada tamanho de $n$. Os eixos Y dos boxplots são independentes entre si, permitindo visualizar a dispersão de cada $n$ individualmente sem compressão de escala.
2. **`5_3_cv_barras.png`**: Gráfico consolidado do Coeficiente de Variação, exibindo o limite rígido de aprovação marcado com uma linha vermelha em **15%**.

---
*Projeto desenvolvido para a disciplina de Engenharia de Programas*