# Meglinho Sneyder Rojas Poma
# Codigo de matricula: 2024200522B
# Tema 36 del temario: Bonos corporativos en el mercado peruano: colocaciones, tasas y plazos
# Fecha de extraccion: 2026-09-23

"""Log de ejecucion y hash SHA-256."""
import hashlib, importlib.util
from datetime import datetime
from pathlib import Path

_r = Path(__file__).resolve().parent / "00_config.py"
_s = importlib.util.spec_from_file_location("config", _r)
cfg = importlib.util.module_from_spec(_s); _s.loader.exec_module(cfg)

def registrar(msg, http=None, filas=None):
    p = [f"[{datetime.now():%Y-%m-%d %H:%M:%S}]", msg]
    if http is not None:  p.append(f"| HTTP {http}")
    if filas is not None: p.append(f"| filas={filas}")
    linea = " ".join(p)
    with open(cfg.LOG, "a", encoding="utf-8") as f:
        f.write(linea + "\n")
    print(linea)

def hash_sha256(ruta):
    d = hashlib.sha256()
    with open(ruta, "rb") as f:
        for b in iter(lambda: f.read(8192), b""):
            d.update(b)
    return d.hexdigest()
