# -*- coding: utf-8 -*-
import warnings
warnings.filterwarnings("ignore")

from sorting import quicksort, shell_sort
from benchmarking import coletar_tempos_para_n
from models import ajustar_modelos
from visualization import gerar_grafico, imprimir_relatorio

def main():
    # ── Configurações ──
    TAMANHOS = [2_000, 8_000, 20_000, 50_000, 100_000]
    N_LISTAS = 50        # listas aleatórias por N
    REP_PILOTO = 35      # repetições para validação de estabilidade
    CV_MAX = 0.15

    ALGORITMOS = {
        "Quicksort":  quicksort,
        "Shell Sort": shell_sort,
    }

    print("=" * 60)
    print("  ANÁLISE EMPÍRICA DE COMPLEXIDADE ALGORÍTMICA")
    print("=" * 60)
    print(f"  Tamanhos de N : {TAMANHOS}")
    print(f"  Listas por N  : {N_LISTAS}")
    print(f"  Repetições    : {REP_PILOTO} (validação estabilidade)")
    print(f"  CV máximo     : {CV_MAX}")
    print("=" * 60)

    resultados_todos = {}

    for nome_alg, fn_sort in ALGORITMOS.items():
        print(f"\n{'─'*60}")
        print(f"  Processando: {nome_alg}")
        print(f"{'─'*60}")

        Ns_validos = []
        tempos_validos = []
        cvs_validos = []

        for n in TAMANHOS:
            print(f"  N = {n:>8,} → coletando...", end="", flush=True)
            tempo_medio, cv, ok = coletar_tempos_para_n(
                fn_sort, n,
                n_listas=N_LISTAS,
                repeticoes_piloto=REP_PILOTO,
                cv_max=CV_MAX,
                seed_base=42
            )
            if ok:
                print(f" tempo={tempo_medio*1e6:.2f}μs  CV={cv:.4f} ✓")
                Ns_validos.append(n)
                tempos_validos.append(tempo_medio)
                cvs_validos.append(cv)
            else:
                print(f" FALHOU (CV={cv:.4f})")

        # Regressão
        regressoes = ajustar_modelos(Ns_validos, tempos_validos)

        resultados_todos[nome_alg] = {
            "Ns": Ns_validos,
            "tempos": tempos_validos,
            "cvs": cvs_validos,
            "regressoes": regressoes,
        }

        imprimir_relatorio(nome_alg, Ns_validos, tempos_validos, cvs_validos, regressoes)

    # Gráfico
    todos_Ns = [n for alg in resultados_todos.values() for n in alg["Ns"]]
    gerar_grafico(resultados_todos, todos_Ns, output_dir=".")

    print("\n" + "="*60)
    print("  CONCLUSÃO FINAL")
    print("="*60)
    for nome_alg, dados in resultados_todos.items():
        melhor = max(dados["regressoes"], key=lambda k: dados["regressoes"][k]["r2"])
        r2 = dados["regressoes"][melhor]["r2"]
        print(f"  {nome_alg:<14} → Melhor ajuste: {melhor}  (R²={r2:.4f})")
    print("="*60)


if __name__ == "__main__":
    main()
