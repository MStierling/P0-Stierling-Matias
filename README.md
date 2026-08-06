# P0-Stierling-Matis

## Proposito general del proyecto

Proyecto del ramo sobre multiplicacion de matrices en Python puro. El proyecto
implementa `mimatmul`, una funcion propia de multiplicacion de matrices, mide su
rendimiento (benchmark) y compara los resultados. Se entrega en dos etapas:

- **P0E1**: configuracion del ambiente, informacion del computador y primera
  version de `mimatmul`.
- **P0E2**: benchmark definitivo, datos finales, grafico y documentacion.

## Sistema operativo

Windows (detalle exacto capturado en `data/system_info.json`).

## Version de Python

Python 3.12.10 (verificada durante la configuracion de P0E1).

## Ambiente virtual

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

## Estructura del proyecto

```
P0-apellido-nombre/
├── AGENTS.md              # Instrucciones para OpenCode
├── README.md              # Este archivo
├── requirements.txt       # Dependencias del proyecto
├── src/
│   ├── mimatmul.py        # Implementacion de mimatmul
│   └── system_info.py     # Informacion del computador
├── data/
│   └── system_info.json   # Informacion generada por system_info.py
└── tests/
    └── test_mimatmul.py   # Pruebas de mimatmul
```

## Estado actual del proyecto

- Ambiente de desarrollo configurado (Python, Git, GitHub, OpenCode, editor,
  ambiente virtual).
- Informacion del computador obtenida en `data/system_info.json`.
- Primera version de `mimatmul` implementada con pruebas iniciales.
- El benchmark definitivo, los datos finales y el grafico se entregaran en P0E2.
