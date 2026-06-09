# Modelar códigos matematicamente

Processo de modelar códigos matematicamente, compreender que a matemática conta são atribuições, comparações e acessos à memória.
* Revisar conceitos
	* Princípio de Indução
	* Método Telescópico 
* Implementar análise FOCA
	* Para casos de for juntos
	* Para casos de while juntos
	* Para casos de for e while juntos
	* Retornar o polinômio para cada caso
* Implementar análise do código do ponto de vista matemático
	* Representar interações e laços de repetições
* Modelar os algoritmos Shell Sort e Quick Sort usando os conceitos
# Análise Empírica e Quantitativa

## Modelo Empírico
A análise empírica do tempo permite, com o tempo, estimar a quantidade de operações executadas por um algoritmo.

$$F(n) = a \log(n) + b$$

### Definições Iniciais
* **Relação da complexidade:** O valor da constante altera o comportamento do código.
* **$N$:** Número de instruções.
* **$n$:** Tamanho da lista (instância do problema).
* **$N(n)$:** Função real que determina o número de operações.

---

## O Modelo FOCA
O modelo FOCA é utilizado para quantificar o comportamento de um algoritmo mapeando suas operações essenciais.

* **F** $\rightarrow$ Chamada de **F**unção
* **O** $\rightarrow$ Operação **O**ritmética (Aritmética)
* **C** $\rightarrow$ Operações de **C**omparação
* **A** $\rightarrow$ **A**tribuições (Explícitas e Implícitas)
    * *Implícita:* Leitura desnecessária.
    * *Explícita:* Escrita na memória (instanciada), ex: $a = i + 1$.

### Cálculo do Tempo e Operações

| Componente | Cálculo do Tempo Total |
| :--- | :--- |
| **Operações ($O$)** | $O \times T_o = T_o$ |
| **Atribuições ($A$)** | $A \times T_a = T_a$ |
| **Comparações ($C$)** | $C \times T_c = T_c$ |

* **Tempo Total ($T$):**
$$T = T_o + T_a + T_c$$
* **Quantidade Total de Operações ($N$):**
$$N = O + A + C + T$$
* **Tempo Médio de cada operação:**
$$\text{Tempo Médio} = \frac{T}{N}$$

---

## Estruturas de Código e Assinaturas

* **Assinatura da função:** $f(a, y)$
* **Chamada recursiva/interna:** $f(i + 1, x)$
* **Retorno e Atribuição:** $p, r = f(\text{args})$

### 1. Bloco Sequencial
As operações de cada instrução são somadas linearmente.

* $\text{inst}_1 \longrightarrow (f, o, c, a)_1$
* $\text{inst}_2 \longrightarrow (f, o, c, a)_2$
* $\text{inst}_3 \longrightarrow (f, o, c, a)_3$

**Exemplo Prático:**
* $\text{inst}_1 \longrightarrow (0, 1, 0, 2) \quad \implies x = 1 + i$
* $\text{inst}_2 \longrightarrow (1, 1, 0, 3) \quad \implies y = f(2 + x)$

### 2. Bloco de Decisão (Condicionais)
Para a análise do **pior caso**, o FOCA adota o caminho que gera o maior número de operações.

$$\text{FOCA} = \max(\text{FOCA}_1, \text{FOCA}_2, \text{FOCA}_3, \dots, \text{FOCA}_n)$$

### 3. Blocos de Repetição (Loops)
Considera a gestão do loop somada às operações úteis multiplicadas pela quantidade de repetições.

$$\text{FOCA}_r = \text{FOCA}_{gl} + X \cdot \text{FOCA}_{in}$$

Onde o número de iterações $X$ (para laços baseados em intervalos) é calculado por:
$$X = \frac{\max(i_f, i_o) - \min(i_f, i_o) + 1}{|S|}$$

*(Onde $i_f$ é o índice final, $i_o$ é o índice inicial e $|S|$ é o tamanho do passo).*

* **Tipos de Loop:** Iterativo e Recursivo.

---

## Exemplos de Aplicação

### Exemplo 1: Sequencial + Decisão
$$\text{FOCA} = \text{FOCA}_{\text{seq}} + \text{FOCA}_{\max(\text{decisao})}$$

### Exemplo 2: Loops Padrão
A gestão do loop (análise padrão) é sempre representada por $3n + 2$.

$$\text{FOCA} = (0, n, n + 1, n + 1)$$

