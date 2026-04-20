import os
import time
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# 1. Especificações da Metodologia
N_VALUES = [100, 500, 1000, 2000, 3000]
REPETITIONS = 30
PERIODS = ['T1', 'T2', 'T3']
LIMIT_CV = 0.15

def run_algorithm(n):
    data = [random.random() for _ in range(n * 10)]
    return sorted(data)

def fmt_sci(ax, axis='y'):
    """Aplica notação científica limpa (×10^x) no eixo especificado."""
    formatter = mticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((0, 0))
    if axis == 'y':
        ax.yaxis.set_major_formatter(formatter)
    else:
        ax.xaxis.set_major_formatter(formatter)

def main():
    data = []
    print("Iniciando a coleta de dados experimentais...")

    for t in PERIODS:
        print(f"[{t}] Executando bateria de testes...")
        for n in N_VALUES:
            for _ in range(5):          # aquecimento
                run_algorithm(n)
            for _ in range(REPETITIONS):
                start = time.perf_counter()
                run_algorithm(n)
                end = time.perf_counter()
                data.append({'Periodo': t, 'n': n, 'Tempo': end - start})

    df = pd.DataFrame(data)
    stats = df.groupby(['Periodo', 'n'])['Tempo'].agg(['mean', 'std']).reset_index()
    stats['CV'] = stats['std'] / stats['mean']

    melhor_periodo = stats.groupby('Periodo')['CV'].mean().idxmin()

    # ------------------------------------------------------------------ #
    # --- Tabela de Validação: Tamanho | T1 | T2 | T3 | Status        --- #
    # ------------------------------------------------------------------ #
    tabela = stats.pivot(index='n', columns='Periodo', values='CV').reset_index()
    tabela.columns.name = None
    tabela = tabela.rename(columns={'n': 'Tamanho'})

    # Garante a ordem das colunas independentemente da ordem de execução
    for col in PERIODS:
        if col not in tabela.columns:
            tabela[col] = float('nan')
    tabela = tabela[['Tamanho'] + PERIODS]

    # Status: Aprovado somente se CV <= LIMIT_CV em TODOS os períodos
    tabela['Status'] = tabela[PERIODS].apply(
        lambda row: 'Aprovado' if (row <= LIMIT_CV).all() else 'Reprovado',
        axis=1
    )

    # Formata CVs como string para exibição (ex.: "0.0842")
    for col in PERIODS:
        tabela[col] = tabela[col].map(lambda v: f'{v:.4f}')

    print("\n--- Tabela de Validação do Setup ---")
    print(tabela.to_string(index=False))
    print()

    print(f" Gerando gráficos...")

    df_plot  = df[df['Periodo'] == melhor_periodo].copy()
    stats_plot = stats[stats['Periodo'] == melhor_periodo].copy()

    # Mantém n numérico para ordenação e cria coluna string para categorias
    df_plot['n_str']    = df_plot['n'].astype(str)
    stats_plot['n_str'] = stats_plot['n'].astype(str)
    n_order  = [str(n) for n in N_VALUES]
    palette  = sns.color_palette("viridis", len(n_order))

    output_dir = 'resultados'
    os.makedirs(output_dir, exist_ok=True)

    # Tema base consistente para todos os gráficos
    sns.set_theme(style="whitegrid", context="talk", font_scale=1.1)
    plt.rcParams.update({
        'axes.spines.top':   False,   # remove bordas desnecessárias
        'axes.spines.right': False,
        'grid.alpha':        0.4,
    })

    # ------------------------------------------------------------------ #
    # --- Gráficos 5.1: BOXPLOTS INDIVIDUAIS (um arquivo por n)       --- #
    # ------------------------------------------------------------------ #
    for n_val, color in zip(N_VALUES, palette):
        n_str  = str(n_val)
        subset = df_plot[df_plot['n_str'] == n_str]

        fig, ax = plt.subplots(figsize=(7, 6))

        sns.boxplot(
            y='Tempo', data=subset,
            color=color, width=0.4,
            linewidth=1.5, ax=ax
        )

        ax.set_title(f'n = {n_val}  ({melhor_periodo})', fontsize=16, pad=12)
        ax.set_ylabel('Tempo de Execução (s)', fontsize=13)
        ax.set_xlabel('')
        ax.set_xticks([])
        fmt_sci(ax, axis='y')

        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'5_1_boxplot_n_{n_val}.png'),
                    dpi=300, bbox_inches='tight')
        plt.close()

    # ------------------------------------------------------------------ #
    # --- Gráfico 5.2: HISTOGRAMAS + KDE em grade (1 × 5 subplots)    --- #
    # ------------------------------------------------------------------ #
    fig, axes = plt.subplots(
        nrows=1, ncols=len(n_order),
        figsize=(30, 9),
        sharey=False
    )

    for ax, n_str, color in zip(axes, n_order, palette):
        subset = df_plot[df_plot['n_str'] == n_str]

        sns.histplot(
            data=subset, x='Tempo',
            kde=True,
            color=color,
            bins=15,
            stat='density',
            linewidth=1.5,
            alpha=0.70,
            ax=ax
        )

        # Linha vertical da média
        media = subset['Tempo'].mean()
        ax.axvline(media, color='crimson', linestyle='--',
                   linewidth=1.8, label=f'Média\n{media:.2e} s')

        ax.set_title(f'n = {int(n_str)}', fontsize=18, pad=10, fontweight='bold')
        ax.set_xlabel('Tempo (s)', fontsize=14, labelpad=8)
        ax.set_ylabel('Densidade' if n_str == n_order[0] else '',
                      fontsize=14, labelpad=8)
        ax.tick_params(axis='both', labelsize=12)
        ax.tick_params(axis='x', labelrotation=30)
        ax.legend(fontsize=11, loc='upper right')
        fmt_sci(ax, axis='x')   # notação científica no eixo X

    fig.suptitle(
        f'5.2 — Distribuição dos Tempos de Execução por n  ({melhor_periodo})',
        fontsize=22, fontweight='bold', y=1.03
    )

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '5_2_histograma.png'),
                dpi=300, bbox_inches='tight')
    plt.close()

    # ------------------------------------------------------------------ #
    # --- Gráfico 5.3: BARRAS DO CV COM LINHA LIMITE (0.15)           --- #
    # ------------------------------------------------------------------ #
    fig, ax = plt.subplots(figsize=(12, 7))

    cv_plot   = stats_plot.sort_values('n')
    n_labels  = cv_plot['n_str'].tolist()
    cv_values = cv_plot['CV'].tolist()

    # Cores condicionais: verde = aprovado, vermelho = reprovado
    bar_colors = [
        '#2ecc71' if cv <= LIMIT_CV else '#e74c3c'
        for cv in cv_values
    ]

    bars = ax.bar(
        n_labels, cv_values,
        color=bar_colors,
        width=0.55,
        edgecolor='white',
        linewidth=1.2,
        zorder=3
    )

    # Linha do limite de aprovação
    ax.axhline(
        LIMIT_CV,
        color='red',
        linestyle='--',
        linewidth=2.2,
        zorder=4,
        label=f'Limite CV = {LIMIT_CV:.0%}'
    )

    # Rótulos de valor no topo de cada barra
    for bar, cv in zip(bars, cv_values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.003,
            f'{cv:.3f}',
            ha='center', va='bottom',
            fontsize=13, fontweight='bold',
            color='#2c3e50'
        )

    # Anotação textual do limite
    ax.annotate(
        f' CV limite = {LIMIT_CV:.0%}',
        xy=(len(n_labels) - 0.5, LIMIT_CV),
        fontsize=12, color='red',
        va='bottom', ha='right',
        fontweight='bold'
    )

    ax.set_title(
        f'5.3 — Coeficiente de Variação por n  ({melhor_periodo})',
        fontsize=20, pad=16, fontweight='bold'
    )
    ax.set_xlabel('Tamanho da Entrada (n)', fontsize=15, labelpad=10)
    ax.set_ylabel('Coeficiente de Variação (CV)', fontsize=15, labelpad=10)
    ax.tick_params(axis='both', labelsize=13)
    ax.set_ylim(0, max(max(cv_values), LIMIT_CV) * 1.35)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1, decimals=1))

    # Legenda com patches coloridos (aprovado / reprovado) + linha limite
    from matplotlib.patches import Patch
    legend_patches = [
        Patch(facecolor='#2ecc71', edgecolor='white', label='Aprovado  (CV ≤ 15%)'),
        Patch(facecolor='#e74c3c', edgecolor='white', label='Reprovado (CV > 15%)'),
    ]
    limit_line_handle = ax.get_legend_handles_labels()[0]  # pega o handle da axhline
    ax.legend(
        handles=legend_patches + limit_line_handle,
        fontsize=12, loc='upper left'
    )

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, '5_3_cv_barras.png'),
                dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Sucesso! Todos os gráficos foram salvos na pasta '{output_dir}'.")

if __name__ == '__main__':
    main()