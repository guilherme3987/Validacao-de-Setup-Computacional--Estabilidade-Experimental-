# -*- coding: utf-8 -*-
import time
import random
import numpy as np

def medir_tempo(sort_fn, arr):
    """Mede o tempo de ordenação de UMA lista (cópia)."""
    copia = arr.copy()
    t0 = time.perf_counter()
    sort_fn(copia)
    return time.perf_counter() - t0


def validar_estabilidade(sort_fn, lista_piloto, repeticoes=35, cv_max=0.15):
    """
    Protocolo de Dupla Validação:
    Ordena a lista piloto 'repeticoes' vezes e verifica o CV.
    Retorna (estavel: bool, cv: float, media: float).
    """
    tempos = [medir_tempo(sort_fn, lista_piloto) for _ in range(repeticoes)]
    media = np.mean(tempos)
    cv = np.std(tempos) / media if media > 0 else 999
    return cv <= cv_max, cv, media


def coletar_tempos_para_n(sort_fn, n, n_listas=50, repeticoes_piloto=35,
                          cv_max=0.15, max_tentativas=5, seed_base=42):
    """
    Coleta o tempo médio representativo para um dado N.
    Retorna (tempo_medio, cv_piloto, sucesso).
    """
    rng = random.Random(seed_base)

    # Gera 50 listas aleatórias
    listas = [[rng.randint(0, 10 * n) for _ in range(n)] for _ in range(n_listas)]

    # ── Passo 1: Validação de estabilidade com a lista piloto ──
    for tentativa in range(max_tentativas):
        estavel, cv, _ = validar_estabilidade(sort_fn, listas[0], repeticoes_piloto, cv_max)
        if estavel:
            break
        print(f"    ⚠  CV={cv:.4f} > {cv_max} → instabilidade. Tentativa {tentativa+1}/{max_tentativas}...")
        time.sleep(0.5)
    else:
        print(f"    ✗  N={n}: não foi possível estabilizar. CV={cv:.4f}")
        return None, cv, False

    # ── Passo 2: Ordenar as 49 listas restantes UMA vez cada ──
    tempos_restantes = [medir_tempo(sort_fn, listas[i]) for i in range(1, n_listas)]

    # ── Passo 3: Média global ──
    tempo_medio = np.mean(tempos_restantes)
    return tempo_medio, cv, True
