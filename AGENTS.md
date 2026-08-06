# AGENTS.md - Instrucciones para OpenCode

## Proposito del proyecto

Proyecto educativo (P0E1/P0E2) que implementa `mimatmul`, una funcion de
multiplicacion de matrices en Python puro, con benchmark y analisis de
rendimiento.

## Reglas basicas

- Mantener el codigo sencillo y claro.
- No inventar mediciones: los datos del benchmark deben provenir de
  ejecuciones reales del codigo.
- No ejecutar comandos destructivos de Git (por ejemplo, force push o
  reset --hard).
- No subir credenciales ni informacion sensible al repositorio.
- Ejecutar las pruebas despues de modificar codigo:

```
python -m pytest
```
