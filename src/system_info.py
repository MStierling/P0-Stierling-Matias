import json
import os
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

RUTA_PROYECTO = Path(__file__).resolve().parent.parent
RUTA_DATA = RUTA_PROYECTO / "data"


def obtener_gpu():
    if platform.system() == "Windows":
        try:
            salida = subprocess.run(
                [
                    "powershell", "-NoProfile", "-Command",
                    "(Get-CimInstance Win32_VideoController).Name",
                ],
                capture_output=True, text=True, timeout=15, check=True,
            ).stdout.strip()
            if salida:
                return [linea for linea in salida.splitlines() if linea]
        except Exception:
            pass
    return []


def obtener_procesador():
    if platform.system() == "Windows":
        try:
            salida = subprocess.run(
                [
                    "powershell", "-NoProfile", "-Command",
                    "(Get-CimInstance Win32_Processor).Name",
                ],
                capture_output=True, text=True, timeout=15, check=True,
            ).stdout.strip()
            if salida:
                return salida
        except Exception:
            pass
    return platform.processor() or "No disponible"


def obtener_informacion():
    info = {
        "sistema_operativo": platform.system(),
        "sistema_operativo_detalle": platform.platform(),
        "arquitectura": platform.machine(),
        "version_python": platform.python_version(),
        "procesador": obtener_procesador(),
        "gpu": obtener_gpu(),
        "nucleos_fisicos": None,
        "procesadores_logicos": None,
        "memoria_ram_total_bytes": None,
        "fecha_captura": datetime.now(timezone.utc).isoformat(),
    }
    if HAS_PSUTIL:
        info["nucleos_fisicos"] = psutil.cpu_count(logical=False)
        info["procesadores_logicos"] = psutil.cpu_count(logical=True)
        info["memoria_ram_total_bytes"] = psutil.virtual_memory().total
    else:
        info["procesadores_logicos"] = os.cpu_count()
    return info


def guardar_informacion(info):
    RUTA_DATA.mkdir(exist_ok=True)
    archivo = RUTA_DATA / "system_info.json"
    archivo.write_text(
        json.dumps(info, indent=4, ensure_ascii=False), encoding="utf-8"
    )
    return archivo


def main():
    info = obtener_informacion()
    archivo = guardar_informacion(info)
    print(json.dumps(info, indent=4, ensure_ascii=False))
    print(f"\nInformacion guardada en: {archivo}")


if __name__ == "__main__":
    main()
