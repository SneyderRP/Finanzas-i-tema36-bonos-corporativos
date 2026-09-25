# Meglinho Sneyder Rojas Poma
# Codigo de matricula: 2024200522B
# Tema 36 del temario: Bonos corporativos en el mercado peruano: colocaciones, tasas y plazos
# Fecha de extraccion: 2026-09-25

"""
VIA 1 - API. Consumo de la API REST publica de BCRPData.

Endpoint: https://estadisticas.bcrp.gob.pe/estadisticas/series/api/
          [codigos]/[formato]/[inicio]/[fin]/[idioma]

No requiere clave. Descarga UNA serie por consulta y guarda cada una por
separado en /datos_crudos/por_variable, para poder cotejarla con la fuente
oficial una por una (numeral 2.4.6). Luego las une en el crudo unificado.
"""
import time, requests, pandas as pd
from utilidades import cfg, registrar

BASE = "https://estadisticas.bcrp.gob.pe/estadisticas/series/api"

# --- Grupo A: los siete instrumentos del panel (cuadros cn-058 y cn-059)
SERIES_BONOS = {
    "coloc_sector_privado":  "PN01064MM",
    "coloc_corporativos":    "PN01081MM",
    "coloc_arrendamiento":   "PN01068MM",
    "coloc_titulizacion":    "PN01084MM",
    "saldo_corporativos":    "PN01101MM",
    "saldo_plazo_hasta_3a":  "PN01103MM",
    "saldo_plazo_3a_5a":     "PN01104MM",
}
# --- Grupo B: contexto de tasas y riesgo
SERIES_CONTEXTO = {
    "tasa_referencia":       "PD04722MM",
    "rend_soberano_10a_pen": "PD31895MM",
    "rend_soberano_10a_usd": "PD31896MM",
    "embig_peru":            "PN01129XM",
    "tasa_pref_corp_90d_mn": "PN07809NM",
    "tasa_corp_mas360_mn":   "PN07842NM",
}
SERIES = {**SERIES_BONOS, **SERIES_CONTEXTO}

MESES = {"ene":1,"feb":2,"mar":3,"abr":4,"may":5,"jun":6,
         "jul":7,"ago":8,"set":9,"sep":9,"oct":10,"nov":11,"dic":12}

def a_fecha(txt):
    """Convierte 'Ene.2015' en el Timestamp 2015-01-01."""
    m, a = txt.replace(".", " ").split()
    return pd.Timestamp(year=int(a), month=MESES[m[:3].lower()], day=1)

def extraer(nombre, codigo):
    """Descarga una serie, verifica su nombre oficial y la guarda."""
    url = f"{BASE}/{codigo}/json/{cfg.BCRP_INICIO}/{cfg.BCRP_FIN}/esp"
    r = requests.get(url, headers={"User-Agent": cfg.USER_AGENT},
                     timeout=cfg.TIMEOUT)
    registrar(f"GET {codigo} -> {url}", http=r.status_code)
    r.raise_for_status()

    d = r.json()
    registrar(f"{nombre} <- {d['config']['series'][0]['name']}")

    t = pd.DataFrame([{"fecha": a_fecha(p["name"]),
                       nombre: pd.to_numeric(p["values"][0], errors="coerce")}
                      for p in d["periods"]]).sort_values("fecha")
    t.to_csv(cfg.DIR_POR_VARIABLE / f"{nombre}__{codigo}.csv",
             index=False, encoding="utf-8")
    registrar(f"Guardado {nombre}__{codigo}.csv", filas=len(t))
    time.sleep(cfg.PAUSA)          # cortesia con la fuente
    return t

def main():
    ancho = None
    for nombre, codigo in SERIES.items():
        t = extraer(nombre, codigo)
        ancho = t if ancho is None else ancho.merge(t, on="fecha", how="outer")

    ancho = ancho.sort_values("fecha")
    # Los crudos se guardan tal como salen de la fuente. No se editan (2.4.5).
    ancho.to_csv(cfg.ARCHIVO_CRUDO, index=False, encoding="utf-8")
    registrar(f"Crudo unificado {cfg.ARCHIVO_CRUDO.name}", filas=len(ancho))
    print(f"\nFilas: {len(ancho)} | Columnas: {len(ancho.columns)}")

if __name__ == "__main__":
    main()
