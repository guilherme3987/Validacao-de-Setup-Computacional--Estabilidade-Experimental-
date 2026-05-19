# -*- coding: utf-8 -*-
import numpy as np
from scipy.optimize import curve_fit

def model_log(n, a, b):
    return a * np.log2(n) + b

def model_linear(n, a, b):
    return a * n + b

def model_nlogn(n, a, b):
    return a * n * np.log2(n) + b

def model_quadratic(n, a, b):
    return a * n**2 + b

def model_cubic(n, a, b):
    return a * n**3 + b

MODELS = {
    "O(log n)":  model_log,
    "O(n)":      model_linear,
    "O(n log n)":model_nlogn,
    "O(n²)":     model_quadratic,
    "O(n³)":     model_cubic,
}

COLORS = {
    "O(log n)":  "#9B59B6",
    "O(n)":      "#2ECC71",
    "O(n log n)": "#E67E22",
    "O(n²)":      "#E74C3C",
    "O(n³)":      "#1ABC9C",
}

def ajustar_modelos(Ns, tempos):
    """Ajusta todos os modelos e retorna parâmetros + R² para cada um."""
    Ns_arr = np.array(Ns, dtype=float)
    T_arr  = np.array(tempos, dtype=float)
    resultados = {}

    for nome, fn in MODELS.items():
        try:
            popt, _ = curve_fit(fn, Ns_arr, T_arr, maxfev=10000, p0=[1e-8, 0])
            T_pred = fn(Ns_arr, *popt)
            ss_res = np.sum((T_arr - T_pred) ** 2)
            ss_tot = np.sum((T_arr - np.mean(T_arr)) ** 2)
            r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
            resultados[nome] = {"params": popt, "r2": r2}
        except Exception as e:
            resultados[nome] = {"params": None, "r2": -999}

    return resultados
