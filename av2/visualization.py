# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os
from models import MODELS, COLORS

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
            cor = COLORS[modelo]
            lw  = 3.0 if modelo == melhor_modelo else 1.2
            ls  = "-" if modelo == melhor_modelo else "--"
            alpha = 1.0 if modelo == melhor_modelo else 0.5
            T_smooth = MODELS[modelo](N_smooth, *info["params"])
            ax.plot(N_smooth, T_smooth * 1e6, color=cor, lw=lw,
                    linestyle=ls, alpha=alpha,
                    label=f"{modelo} (R²={info['r2']:.4f})")

        ax.set_title(f"Ajuste Assintótico: {nome_alg}",
                     color="#F0F0F0", fontsize=15, fontweight="bold", pad=15)
        ax.set_xlabel("Tamanho da lista (N)", color="#AAAAAA", fontsize=12)
        ax.set_ylabel("Tempo médio (μs)", color="#AAAAAA", fontsize=12)
        ax.tick_params(colors="#AAAAAA")
        for spine in ax.spines.values():
            spine.set_edgecolor("#333355")

        ax.legend(fontsize=10, loc="upper left",
                  facecolor="#12141E", edgecolor="#333355",
                  labelcolor="#DDDDDD", framealpha=0.9)

        filename = f"dispersao_{nome_alg.lower().replace(' ', '_')}.png"
        output_path = os.path.join(output_dir, filename)
        plt.savefig(output_path, dpi=160, bbox_inches="tight", facecolor=fig.get_facecolor())
        plt.close()
        print(f"✅ Gráfico salvo em {output_path}")

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
