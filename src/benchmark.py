import csv
import sys
import threading
import time
from collections import defaultdict
from pathlib import Path

RUTA_PROYECTO = Path(__file__).resolve().parent.parent
if str(RUTA_PROYECTO) not in sys.path:
    sys.path.insert(0, str(RUTA_PROYECTO))

import psutil

import numpy as np

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.mimatmul import mimatmul

RUTA_DATA = RUTA_PROYECTO / "data"
RUTA_FIGURES = RUTA_PROYECTO / "figures"
ARCHIVO_CSV = RUTA_DATA / "benchmark_results.csv"
ARCHIVO_GRAFICO = RUTA_FIGURES / "benchmark.png"

TAMANOS = [16, 32, 64, 128]
REPETICIONES = 3

RNG = np.random.default_rng(42)

METODOS = [
    ("mimatmul", lambda A, B: mimatmul(A.tolist(), B.tolist())),
    ("numpy", lambda A, B: A @ B),
]


def medir(metodo, n):
    A = RNG.random((n, n))
    B = RNG.random((n, n))
    metodo(A, B)
    tiempos = []
    for _ in range(REPETICIONES):
        t0 = time.perf_counter()
        metodo(A, B)
        t1 = time.perf_counter()
        tiempos.append(t1 - t0)
    return tiempos


def monitorear_recurso(muestras, parar):
    proc = psutil.Process()
    proc.cpu_percent(interval=None)
    while not parar.is_set():
        muestras.append((proc.cpu_percent(interval=None), proc.memory_info().rss))
        parar.wait(0.05)


def graficar(resultados):
    medias = defaultdict(list)
    for metodo, n, rep, tiempo in resultados:
        medias[(metodo, n)].append(tiempo)

    plt.figure(figsize=(8, 5))
    for nombre, _ in METODOS:
        tamanos = []
        tiempos_medios = []
        for n in TAMANOS:
            valores = medias[(nombre, n)]
            tamanos.append(n)
            tiempos_medios.append(sum(valores) / len(valores))
        plt.plot(tamanos, tiempos_medios, marker="o", label=nombre)
        repeticiones = [(n, t) for m, n, _, t in resultados if m == nombre]
        plt.scatter(
            [n for n, _ in repeticiones],
            [t for _, t in repeticiones],
            alpha=0.4,
        )

    plt.xlabel("Tamano de la matriz (n x n)")
    plt.ylabel("Tiempo (segundos)")
    plt.title("Benchmark: mimatmul vs NumPy")
    plt.yscale("log")
    plt.legend()
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.savefig(ARCHIVO_GRAFICO, dpi=150)
    plt.close()


def main():
    RUTA_DATA.mkdir(exist_ok=True)
    RUTA_FIGURES.mkdir(exist_ok=True)

    resultados = []
    muestras = []
    parar = threading.Event()
    hilo = threading.Thread(
        target=monitorear_recurso, args=(muestras, parar), daemon=True
    )
    hilo.start()

    for nombre, metodo in METODOS:
        for n in TAMANOS:
            print(f"Midiendo {nombre} con n={n} ...")
            for rep, tiempo in enumerate(medir(metodo, n), start=1):
                resultados.append([nombre, n, rep, tiempo])

    parar.set()
    hilo.join(timeout=1)

    with open(ARCHIVO_CSV, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["metodo", "tamanio", "repeticion", "tiempo_s"])
        escritor.writerows(resultados)

    cpu_max = max((m for m, _ in muestras), default=0.0)
    ram_max = max((r for _, r in muestras), default=0)

    print("\nResumen:")
    for nombre, _ in METODOS:
        for n in TAMANOS:
            tiempos = [t for m, nn, _, t in resultados if m == nombre and nn == n]
            media = sum(tiempos) / len(tiempos)
            print(f"{nombre:9s} n={n:4d} media={media:.6f} s")

    print(f"\nCPU maxima del proceso: {cpu_max:.1f} %")
    print(f"RAM maxima del proceso: {ram_max / 2**30:.3f} GiB")

    graficar(resultados)

    print(f"\nDatos guardados en: {ARCHIVO_CSV}")
    print(f"Grafico guardado en: {ARCHIVO_GRAFICO}")


if __name__ == "__main__":
    main()
