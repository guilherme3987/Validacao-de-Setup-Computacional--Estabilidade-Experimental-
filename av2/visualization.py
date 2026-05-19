# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os
from models import MODELS, COLORS

def gerar_grafico(resultados_algoritmos, Ns_todos, output_dir="."):
    """
    Gera o painel completo:
    - Linha 1: gráfico de dispersão + curvas para cada algoritmo
    - Linha 2: barras de R² para cada algoritmo
    - Linha 3: comparação direta dos tempos reais
    """
    algoritmos = list(resultados_algoritmos.keys())
    n_alg = len(algoritmos)

    fig = plt.figure(figsize=(18, 15))
    fig.patch.set_facecolor("#0F1117")

    gs = gridspec.GridSpec(3, n_alg, figure=fig,
                           hspace=0.45, wspace=0.35,
                           height_ratios=[2.5, 1.2, 1.8])

    N_smooth = np.linspace(min(Ns_todos), max(Ns_todos), 400)

    # ── Linha 1: Dispersão + curvas de regressão ──
    for col, nome_alg in enumerate(algoritmos):
        ax = fig.add_subplot(gs[0, col])
        ax.set_facecolor("#1A1D27")
        dados = resultados_algoritmos[nome_alg]
        Ns_arr = np.array(dados["Ns"], dtype=float)
        T_arr  = np.array(dados["tempos"], dtype=float)
        regs   = dados["regressoes"]

        # Pontos reais
        ax.scatter(Ns_arr, T_arr * 1e6, color="#FFFFFF", s=80, zorder=10,
                   edgecolors="#F39C12", linewidths=1.5, label="Dados reais")

        melhor_modelo = max(regs, key=lambda k: regs[k]["r2"])

        for modelo, info in regs.items():
            if info["params"] is None:
                continue
            cor = COLORS[modelo]
            lw  = 3.0 if modelo == melhor_modelo else 1.2
            ls  = "-" if modelo == melhor_modelo else "--"
            alpha = 1.0 if modelo == melhor_modelo else 0.5
            T_smooth = MODELS[modelo](N_smooth, *info["params"])
            ax.plot(N_smooth, T_smooth * 1e6, color=cor, lw=lw,
                    linestyle=ls, alpha=alpha,
                    label=f"{modelo} (R²={info['r2']:.4f})")

        ax.set_title(f"{'─'*4} {nome_alg} {'─'*4}",
                     color="#F0F0F0", fontsize=13, fontweight="bold", pad=10)
        ax.set_xlabel("Tamanho da lista (N)", color="#AAAAAA", fontsize=10)
        ax.set_ylabel("Tempo médio (μs)", color="#AAAAAA", fontsize=10)
        ax.tick_params(colors="#AAAAAA")
        for spine in ax.spines.values():
            spine.set_edgecolor("#333355")

        leg = ax.legend(fontsize=7.5, loc="upper left",
                        facecolor="#12141E", edgecolor="#333355",
                        labelcolor="#DDDDDD", framealpha=0.9)
        ax.xaxis.get_offset_text().set_color("#AAAAAA")

    # ── Linha 2: Barras de R² ──
    for col, nome_alg in enumerate(algoritmos):
        ax = fig.add_subplot(gs[1, col])
        ax.set_facecolor("#1A1D27")
        regs = resultados_algoritmos[nome_alg]["regressoes"]
        nomes_m = list(regs.keys())
        r2s = [max(0, regs[m]["r2"]) for m in nomes_m]
        cores = [COLORS[m] for m in nomes_m]
        bars = ax.bar(range(len(nomes_m)), r2s, color=cores, edgecolor="#222233",
                      linewidth=0.8, alpha=0.9)
        ax.set_xticks(range(len(nomes_m)))
        ax.set_xticklabels(nomes_m, rotation=30, ha="right",
                           color="#AAAAAA", fontsize=8)
        ax.set_ylim(0, 1.05)
        ax.set_ylabel("R²", color="#AAAAAA", fontsize=10)
        ax.set_title(f"R² por Modelo – {nome_alg}",
                     color="#F0F0F0", fontsize=10, fontweight="bold")
        ax.tick_params(colors="#AAAAAA")
        ax.axhline(0.99, color="#F39C12", lw=1.2, ls="--", alpha=0.7, label="R²=0.99")
        for spine in ax.spines.values():
            spine.set_edgecolor("#333355")

        for bar, r2 in zip(bars, r2s):
            ax.text(bar.get_x() + bar.get_width() / 2, r2 + 0.01,
                    f"{r2:.3f}", ha="center", va="bottom",
                    color="#FFFFFF", fontsize=7.5, fontweight="bold")

    # ── Linha 3: Comparação direta dos tempos reais ──
    ax_comp = fig.add_subplot(gs[2, :])
    ax_comp.set_facecolor("#1A1D27")
    cores_alg = ["#3498DB", "#E74C3C", "#2ECC71", "#F39C12"]
    for idx, nome_alg in enumerate(algoritmos):
        dados = resultados_algoritmos[nome_alg]
        Ns_arr = np.array(dados["Ns"], dtype=float)
        T_arr  = np.array(dados["tempos"], dtype=float)
        ax_comp.plot(Ns_arr, T_arr * 1e6,
                     color=cores_alg[idx % len(cores_alg)],
                     marker="o", lw=2.5, markersize=8, label=nome_alg)

    ax_comp.set_title("Comparação Direta: Tempo Real por Algoritmo",
                      color="#F0F0F0", fontsize=12, fontweight="bold")
    ax_comp.set_xlabel("Tamanho da lista (N)", color="#AAAAAA", fontsize=11)
    ax_comp.set_ylabel("Tempo médio (μs)", color="#AAAAAA", fontsize=11)
    ax_comp.tick_params(colors="#AAAAAA")
    for spine in ax_comp.spines.values():
        spine.set_edgecolor("#333355")
    ax_comp.legend(fontsize=10, facecolor="#12141E",
                   edgecolor="#333355", labelcolor="#DDDDDD")

    # Título geral
    fig.suptitle(
        "Análise Empírica de Complexidade — Quicksort vs Shell Sort\n"
        "Metodologia: Dupla Validação (CV ≤ 0.15) + Regressão Não-Linear (scipy.curve_fit)",
        color="#FFFFFF", fontsize=14, fontweight="bold", y=0.98
    )

    output_path = os.path.join(output_dir, "sort_complexity.png")
    plt.savefig(output_path, dpi=160, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"\n✅ Gráfico salvo em {output_path}")


def imprimir_relatorio(nome_alg, Ns, tempos, cvs, regressoes):
    print(f"\n{'═'*60}")
    print(f"  ALGORITMO: {nome_alg}")
    print(f"{'═'*60}")
    print(f"  {'N':>10}  {'Tempo Médio (μs)':>18}  {'CV Piloto':>12}")
    print(f"  {'─'*10}  {'─'*18}  {'─'*12}")
    for n, t, cv in zip(Ns, tempos, cvs):
        print(f"  {n:>10,}  {t*1e6:>18.2f}  {cv:>12.4f}")

    print(f"\n  {'Modelo':<14}  {'R²':>8}  {'Veredito'}")
    print(f"  {'─'*14}  {'─'*8}  {'─'*20}")
    melhor = max(regressoes, key=lambda k: regressoes[k]["r2"])
    for modelo, info in regressoes.items():
        flag = "◀ MELHOR AJUSTE" if modelo == melhor else ""
        print(f"  {modelo:<14}  {info['r2']:>8.4f}  {flag}")
