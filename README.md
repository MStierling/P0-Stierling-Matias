# P0-Stierling-Matias

## Propósito general del proyecto

Proyecto del ramo sobre multiplicación de matrices en Python puro. El proyecto
implementa `mimatmul`, una función propia de multiplicación de matrices, compara
sus resultados con NumPy y mide su rendimiento (benchmark). Se entrega en dos
etapas:

- **P0E1**: configuración del ambiente, información del computador y primera
  versión de `mimatmul`.
- **P0E2**: `mimatmul` completa con pruebas, benchmark definitivo, datos finales,
  gráfico y documentación.

## Características del computador

Datos reales capturados en `data/system_info.json`.

| Característica | Valor |
|---|---|
| Sistema operativo | Windows 11 (10.0.26200) |
| Arquitectura | AMD64 (x64) |
| Procesador | Intel(R) Core(TM) 5 210H |
| Núcleos físicos | 8 |
| Procesadores lógicos | 12 |
| Memoria RAM total | 8 GB (7.61 GiB) |
| GPU | Intel(R) Graphics, NVIDIA GeForce RTX 3050 6GB Laptop GPU |
| Versión de Python | 3.12.10 |

## Reproducibilidad

Los comandos que siguen permiten clonar el proyecto y reproducir los resultados.

Clonar o descargar el repositorio:

```
git clone https://github.com/MStierling/P0-Stierling-Matias.git
cd P0-Stierling-Matias
```

Crear el ambiente virtual:

```
python -m venv .venv
```

Activar el ambiente virtual:

```
.venv\Scripts\activate
```

Instalar las dependencias:

```
pip install -r requirements.txt
```

Ejecutar las pruebas:

```
python -m pytest
```

Ejecutar el benchmark (genera el CSV y el gráfico):

```
python src/benchmark.py
```

Obtener la información del computador:

```
python src/system_info.py
```

## Estructura del proyecto

```
P0-Stierling-Matias/
├── AGENTS.md              # Instrucciones para OpenCode
├── README.md              # Este archivo
├── requirements.txt       # Dependencias del proyecto
├── conftest.py            # Configuración de pytest
├── src/
│   ├── mimatmul.py        # Implementación de mimatmul
│   ├── system_info.py     # Información del computador
│   └── benchmark.py       # Benchmark mimatmul vs NumPy
├── tests/
│   └── test_mimatmul.py   # Pruebas de mimatmul
├── data/
│   ├── system_info.json       # Información generada por system_info.py
│   └── benchmark_results.csv  # Mediciones del benchmark
└── figures/
    └── benchmark.png      # Gráfico del benchmark
```

## Implementación de mimatmul

`src/mimatmul.py` implementa la multiplicación de matrices con ciclos explícitos
de Python (triple ciclo `for`), sin usar NumPy ni operadores de álgebra lineal
(`@`, `np.matmul`, `np.dot`, `np.einsum`). Funciona con matrices cuadradas y
rectangulares, comprueba las dimensiones y lanza un `ValueError` con un mensaje
claro cuando las dimensiones son incompatibles.

Las pruebas en `tests/test_mimatmul.py` cubren: un caso conocido, matrices
cuadradas, matrices rectangulares, dimensiones incompatibles y comparación de
resultados contra NumPy. Todas se ejecutan con `pytest` y terminan
exitosamente.

## Resultados del benchmark

Mediciones reales realizadas en este computador. Cada tiempo es el promedio de
3 repeticiones, con ejecución de calentamiento previa. Matrices `float64`.

| Tamaño (n×n) | mimatmul (s) | NumPy `A @ B` (s) | Cuánto más lento |
|---|---|---|---|
| 16 | 0.000168 | 0.000005 | ~35× |
| 32 | 0.001232 | 0.000007 | ~180× |
| 64 | 0.009795 | 0.000012 | ~788× |
| 128 | 0.080756 | 0.000272 | ~297× |

Los datos completos (método, tamaño, repetición y tiempo medido) están en
`data/benchmark_results.csv`. El gráfico generado está en
`figures/benchmark.png`.

## Observaciones de rendimiento

1. **¿mimatmul parece utilizar uno o varios núcleos?**
   Uno solo. Durante el benchmark el proceso llegó a ~100% de CPU, lo que
   equivale a un núcleo. `mimatmul` es Python puro con ciclos secuenciales en un
   solo hilo (limitado por el GIL de Python).

2. **¿NumPy parece utilizar uno o varios núcleos?**
   Para las matrices pequeñas del benchmark (n ≤ 128) parecía usar un núcleo,
   porque los tiempos son de microsegundos y no conviene paralelizar. Con una
   matriz más grande (n = 2000, medición adicional) la CPU del proceso alcanzó
   ~748%, es decir, **NumPy usa varios núcleos** para matrices grandes a través
   de las bibliotecas BLAS.

3. **¿Por qué NumPy es más rápido?**
   NumPy ejecuta la multiplicación en código C optimizado (BLAS/LAPACK), trabaja
   sobre arreglos contiguos en memoria y aprovecha instrucciones vectorizadas y
   múltiples núcleos. `mimatmul` recorre cada elemento con ciclos interpretados
   de Python, lo que tiene mucho más costo por operación.

4. **¿Por qué las repeticiones no entregan exactamente el mismo tiempo?**
   Por el ruido del sistema: otros procesos compitiendo por la CPU, cambios de
   frecuencia del procesador, estado de la caché y overhead del reloj. En
   tamaños pequeños el overhead relativo es mayor y las variaciones se notan más.

5. **¿Cuál es aproximadamente la matriz cuadrada de mayor tamaño que cabría en
   la RAM libre del computador?**
   Una matriz `n×n` de `float64` ocupa `8·n²` bytes. Con la RAM total de
   7.61 GiB, el límite teórico sería `n ≈ 32000`. Considerando la RAM libre
   observada en el momento de la captura (~0.47 GiB), el tamaño realista sería
   `n ≈ 7900`. En la práctica también hay que dejar RAM para el sistema y los
   datos de entrada, por lo que conviene usar tamaños mucho menores.

## Uso de OpenCode

1. **¿Qué parte realizó correctamente el agente?**
   El agente creó la estructura completa del proyecto, implementó
   `system_info.py`, `mimatmul.py`, las pruebas, el benchmark con su CSV y el
   gráfico, y redactó el README y AGENTS.md. También detectó y corrigió errores
   de ejecución (por ejemplo, que `mimatmul` recibiera arreglos de NumPy y que
   faltara llamar a la función `graficar`).

2. **¿Qué parte tuvo que corregir o modificar?**
   El nombre del repositorio en GitHub: el remote local apuntaba a un nombre
   distinto del real (`P0-Stierling-Matias`), lo que produjo el error
   "Repository not found". Además, los pasos de autenticación y publicación en
   GitHub (renombrar el repositorio y hacer el push) se hicieron manualmente.

3. **¿Qué archivo comprende mejor después del proyecto?**
   `src/mimatmul.py`: es el más corto y claro, con un triple ciclo explícito que
   implementa directamente la definición de la multiplicación de matrices.

4. **¿Qué parte del código todavía le resulta menos clara?**
   El monitoreo de CPU/RAM con hilos (`threading`) en `src/benchmark.py`, porque
   combina concurrencia con la medición de tiempos. También la configuración del
   backend de matplotlib para generar el gráfico.

## Estado del proyecto

- **P0E1 (entregado)**: ambiente configurado, información del computador e
  inicio de `mimatmul`.
- **P0E2 (final)**: `mimatmul` completa, 8 pruebas que pasan, benchmark con
  datos reales en CSV, gráfico final y documentación completa.
