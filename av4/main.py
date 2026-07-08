# -*- coding: utf-8 -*-
import time
import random
import numpy as np
from sorting import quicksort, quicksort_ops, shell_sort, shell_sort_ops
from visualization import plot_ops_vs_n, plot_comparacao_normalizada

TAMANHOS = [1000, 2000, 5000, 10000, 20000, 50000, 100000]
N_LISTAS = 20
SEED = 42

def coletar_ops(fn_ops, n, n_listas=N_LISTAS):
    rng = random.Random(SEED)
    ops_list = []
    for _ in range(n_listas):
        arr = [rng.randint(0, 10 * n) for _ in range(n)]
        _, ops = fn_ops(arr)
        ops_list.append(ops)
    return np.mean(ops_list)

def coletar_tempos(fn, n, n_listas=N_LISTAS):
    rng = random.Random(SEED)
    tempos = []
    for _ in range(n_listas):
        arr = [rng.randint(0, 10 * n) for _ in range(n)]
        copia = arr.copy()
        t0 = time.perf_counter()
        fn(copia)
        tempos.append(time.perf_counter() - t0)
    return np.mean(tempos)

def main():
    print("=" * 60)
    print("  ANÁLISE DE OPERAÇÕES TOTAIS vs N")
    print("=" * 60)
    print(f"  Tamanhos: {TAMANHOS}")
    print(f"  Listas por N: {N_LISTAS}")
    print("=" * 60)

    resultados = {}

    for nome, fn_sort, fn_ops in [
        ("Quicksort", quicksort, quicksort_ops),
        ("Shell Sort", shell_sort, shell_sort_ops),
    ]:
        print(f"\n  {nome}:")
        Ns, ops_vals, tempo_vals = [], [], []
        for n in TAMANHOS:
            media_ops = coletar_ops(fn_ops, n)
            media_tempo = coletar_tempos(fn_sort, n)
            Ns.append(n)
            ops_vals.append(media_ops)
            tempo_vals.append(media_tempo)
            print(f"    N={n:>7,}  →  ops={media_ops:>12,.0f}  tempo={media_tempo*1e6:>8.2f}us")
        resultados[nome] = {"Ns": Ns, "ops": ops_vals, "tempos": tempo_vals}

    plot_ops_vs_n(resultados)
    plot_comparacao_normalizada(resultados)

if __name__ == "__main__":
    main()
