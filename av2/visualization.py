# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.interpolate import make_interp_spline
from models import MODELS, COLORS

# Equações formatadas com os coeficientes numéricos
EQUACOES = {
    "O(log n)":   lambda a, b: f"T(n) = {a:.4e} · log₂(n) + {b:.4e}",
    "O(n)":       lambda a, b: f"T(n) = {a:.4e} · n + {b:.4e}",
    "O(n log n)": lambda a, b: f"T(n) = {a:.4e} · n·log₂(n) + {b:.4e}",
    "O(n²)":      lambda a, b: f"T(n) = {a:.4e} · n² + {b:.4e}",
    "O(n³)":      lambda a, b: f"T(n) = {a:.4e} · n³ + {b:.4e}",
}

# Cores fixas por algoritmo para o gráfico comparativo
CORES_ALG = {
    "Quicksort":  "#2ECC71",
    "Shell Sort": "#E74C3C",
}
MARCADORES_ALG = {
    "Quicksort":  "o",
    "Shell Sort": "s",
}


def gerar_graficos_separados(resultados_algoritmos, Ns_todos, output_dir="resultados/imagens"):
    """
    Gera um gráfico de dispersão com os 5 pontos reais e sobrepõe
    as 5 curvas matemáticas separadamente para cada algoritmo.
    """
    os.makedirs(output_dir, exist_ok=True)
    N_smooth = np.linspace(min(Ns_todos), max(Ns_todos), 400)

    for nome_alg, dados in resultados_algoritmos.items():
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor("#0F1117")
        ax.set_facecolor("#1A1D27")

        Ns_arr = np.array(dados["Ns"], dtype=float)
        T_arr  = np.array(dados["tempos"], dtype=float)
        regs   = dados["regressoes"]

        # Pontos reais
        ax.scatter(Ns_arr, T_arr * 1e6, color="#FFFFFF", s=100, zorder=10,
                   edgecolors="#F39C12", linewidths=2, label="Dados reais (5 pontos)")

        melhor_modelo = max(regs, key=lambda k: regs[k]["r2"])

        for modelo, info in regs.items():
            if info["params"] is None:
                continue
            cor   = COLORS[modelo]
            lw    = 3.0 if modelo == melhor_modelo else 1.2
            ls    = "-"  if modelo == melhor_modelo else "--"
            alpha = 1.0  if modelo == melhor_modelo else 0.5
            T_smooth = MODELS[modelo](N_smooth, *info["params"])
            ax.plot(N_smooth, T_smooth * 1e6, color=cor, lw=lw,
                    linestyle=ls, alpha=alpha,
                    label=f"{modelo} (R²={info['r2']:.4f})")

        # Equação do melhor ajuste como anotação no gráfico
        best_info = regs[melhor_modelo]
        if best_info["params"] is not None:
            a, b = best_info["params"]
            eq_str = EQUACOES[melhor_modelo](a, b)
            ax.annotate(
                f"Melhor ajuste: {melhor_modelo}\n{eq_str}",
                xy=(0.03, 0.97), xycoords="axes fraction",
                fontsize=9, color="#F39C12",
                va="top", ha="left",
                bbox=dict(boxstyle="round,pad=0.4", fc="#12141E", ec="#F39C12", alpha=0.85),
            )

        ax.set_title(f"Ajuste Assintótico: {nome_alg}",
                     color="#F0F0F0", fontsize=15, fontweight="bold", pad=15)
        ax.set_xlabel("Tamanho da lista (N)", color="#AAAAAA", fontsize=12)
        ax.set_ylabel("Tempo médio (μs)", color="#AAAAAA", fontsize=12)
        ax.tick_params(colors="#AAAAAA")
        for spine in ax.spines.values():
            spine.set_edgecolor("#333355")

        ax.legend(fontsize=10, loc="lower right",
                  facecolor="#12141E", edgecolor="#333355",
                  labelcolor="#DDDDDD", framealpha=0.9)

        filename = f"dispersao_{nome_alg.lower().replace(' ', '_')}.png"
        output_path = os.path.join(output_dir, filename)
        plt.savefig(output_path, dpi=160, bbox_inches="tight", facecolor=fig.get_facecolor())
        plt.close()
        print(f"✅ Gráfico salvo em {output_path}")


def gerar_grafico_comparativo(resultados_algoritmos, output_dir="resultados/imagens"):
    """
    Plota os tempos médios de ambos os algoritmos no mesmo eixo,
    sem curvas de regressão — apenas os pontos reais unidos por splines cúbicas.
    """
    os.makedirs(output_dir, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor("#0F1117")
    ax.set_facecolor("#1A1D27")

    for nome_alg, dados in resultados_algoritmos.items():
        Ns_arr = np.array(dados["Ns"], dtype=float)
        T_arr  = np.array(dados["tempos"], dtype=float) * 1e6   # → μs
        cor     = CORES_ALG.get(nome_alg, "#FFFFFF")
        marcador = MARCADORES_ALG.get(nome_alg, "o")

        # Spline cúbica suave entre os pontos medidos
        if len(Ns_arr) >= 4:
            N_smooth = np.linspace(Ns_arr.min(), Ns_arr.max(), 500)
            spline   = make_interp_spline(Ns_arr, T_arr, k=3)
            T_smooth = spline(N_smooth)
            ax.plot(N_smooth, T_smooth, color=cor, lw=2.2, alpha=0.85)
        else:
            ax.plot(Ns_arr, T_arr, color=cor, lw=2.2, alpha=0.85)

        ax.scatter(Ns_arr, T_arr, color=cor, s=110, zorder=10,
                   edgecolors="#FFFFFF", linewidths=1.5,
                   marker=marcador, label=nome_alg)

        # Anotação com o tempo no último ponto
        ax.annotate(
            f"{T_arr[-1]:,.0f} μs",
            xy=(Ns_arr[-1], T_arr[-1]),
            xytext=(8, 0), textcoords="offset points",
            fontsize=9, color=cor, va="center",
        )

    ax.set_title("Comparação de Tempo Médio: Quicksort vs Shell Sort",
                 color="#F0F0F0", fontsize=15, fontweight="bold", pad=15)
    ax.set_xlabel("Tamanho da lista (N)", color="#AAAAAA", fontsize=12)
    ax.set_ylabel("Tempo médio (μs)", color="#AAAAAA", fontsize=12)
    ax.tick_params(colors="#AAAAAA")
    for spine in ax.spines.values():
        spine.set_edgecolor("#333355")

    ax.legend(fontsize=11, loc="upper left",
              facecolor="#12141E", edgecolor="#333355",
              labelcolor="#DDDDDD", framealpha=0.9)

    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}"))

    output_path = os.path.join(output_dir, "comparativo_tempos.png")
    plt.savefig(output_path, dpi=160, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"✅ Gráfico comparativo salvo em {output_path}")


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

    # Coeficientes numéricos do melhor ajuste
    best_info = regressoes[melhor]
    if best_info["params"] is not None:
        a, b = best_info["params"]
        eq_str = EQUACOES[melhor](a, b)
        print(f"\n  Equação do melhor ajuste ({melhor}):")
        print(f"    {eq_str}  [T em segundos]")
        print(f"    a = {a:.6e}  (coeficiente principal)")
        print(f"    b = {b:.6e}  (constante aditiva)")