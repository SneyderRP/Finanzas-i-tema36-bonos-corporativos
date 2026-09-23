# Meglinho Sneyder Rojas Poma
# Codigo de matricula: 2024200522B
# Tema 36 del temario: Bonos corporativos en el mercado peruano: colocaciones, tasas y plazos
# Fecha de extraccion: 2026-09-23

"""
VIA 1 - API. Extraccion de las cinco series diarias de BCRPData.

Endpoint oficial:
  https://estadisticas.bcrp.gob.pe/estadisticas/series/api/
      [codigo]/[formato]/[inicio]/[fin]/[idioma]

No requiere clave: BCRPData es una API publica de acceso libre.

Cada serie se descarga por SEPARADO y se guarda en /datos_crudos/diarias, para
poder cotejarla contra la fuente oficial una por una (numeral 2.4.6, paso 1).
Al final se unen por fecha en el crudo unificado.

La consulta esta CONGELADA: INICIO y FIN son constantes, nunca la fecha del dia
(numeral 2.4.5), de modo que la reejecucion produce el mismo archivo.

Los datos crudos se guardan TAL COMO SALEN de la fuente y no se editan.
"""

import re, time, requests, pandas as pd
from pathlib import Path
from datetime import datetime

RAIZ = Path(__file__).resolve().parent.parent
DEST = RAIZ / "datos_crudos" / "diarias"
DEST.mkdir(parents=True, exist_ok=True)
LOG = RAIZ / "log_ejecucion.txt"

UA = ("UNCP-FacultadEconomia-FinanzasI/1.0 (trabajo academico; "
      "contacto: e_2024200522B@uncp.edu.pe)")
BASE = "https://estadisticas.bcrp.gob.pe/estadisticas/series/api"
INICIO, FIN = "2011-1-1", "2025-12-31"
PAUSA, TIMEOUT = 1.5, 90

SERIES = {
    "Y_rend_soberano_10a": "PD31893DD",  # Rendimiento bono peruano 10 anos (S/)
    "X1_tasa_referencia":  "PD12301MD",  # Tasa de referencia de politica monetaria
    "X2_treasury_10a":     "PD04719XD",  # Bonos del Tesoro EE.UU. 10 anos
    "X3_embig_peru":       "PD04709XD",  # Spread EMBIG Peru (pbs)
    "X4_interbancaria":    "PD04692MD",  # Tasa interbancaria, S/
}

MESES = {"ene":1,"feb":2,"mar":3,"abr":4,"may":5,"jun":6,
         "jul":7,"ago":8,"set":9,"sep":9,"oct":10,"nov":11,"dic":12}


def a_fecha(txt):
    """
    Convierte el periodo diario del BCRP en Timestamp.

    El formato varia entre series (puntos, espacios, anio de dos o cuatro
    digitos), asi que se separa por cualquier delimitador y se identifica
    cada parte por su contenido en lugar de por su posicion.
    """
    partes = [p for p in re.split(r"[.\s\-/]+", txt.strip()) if p]
    dia = mes = anio = None
    for p in partes:
        pl = p.lower()[:3]
        if pl in MESES:
            mes = MESES[pl]
        elif p.isdigit():
            if len(p) == 4:   anio = int(p)
            elif dia is None: dia = int(p)
            else:             anio = 2000 + int(p)
    if anio is not None and anio < 100:
        anio += 2000
    return pd.Timestamp(year=anio, month=mes, day=dia)


def log(msg):
    """Registra en log_ejecucion.txt: entregable obligatorio (numeral 2.4.2)."""
    linea = f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}"
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(linea + "\n")
    print(linea)


def main():
    ancho = None
    for nombre, cod in SERIES.items():
        url = f"{BASE}/{cod}/json/{INICIO}/{FIN}/esp"
        r = requests.get(url, headers={"User-Agent": UA}, timeout=TIMEOUT)
        log(f"GET {cod} -> {url} | HTTP {r.status_code}")
        r.raise_for_status()

        d = r.json()
        # Se registra el nombre oficial devuelto: confirma que el codigo trajo
        # la serie esperada y no otra.
        log(f"{nombre} <- {d['config']['series'][0]['name']}")

        t = pd.DataFrame([{"fecha": a_fecha(p["name"]),
                           nombre: pd.to_numeric(p["values"][0], errors="coerce")}
                          for p in d["periods"]]).sort_values("fecha")
        t.to_csv(DEST / f"{nombre}__{cod}.csv", index=False, encoding="utf-8")
        log(f"Guardado {nombre}__{cod}.csv | filas={len(t)}")

        ancho = t if ancho is None else ancho.merge(t, on="fecha", how="outer")
        time.sleep(PAUSA)   # cortesia con la fuente (numeral 2.4.8)

    ancho = ancho.sort_values("fecha")
    salida = RAIZ / "datos_crudos" / "datos_crudos_diario_2024200522B.csv"
    ancho.to_csv(salida, index=False, encoding="utf-8")
    log(f"Crudo diario unificado | filas={len(ancho)}")
    print(f"\nFilas: {len(ancho)} | Columnas: {len(ancho.columns)}")


if __name__ == "__main__":
    main()
