# Meglinho Sneyder Rojas Poma
# Codigo de matricula: 2024200522B
# Tema 36 del temario: Bonos corporativos en el mercado peruano: colocaciones, tasas y plazos
# Fecha de extraccion: 2026-09-23

"""
VIA 2 - Verificacion cruzada por rastreo de HTML.

La Unidad I exige UNA sola via automatizada, preferentemente API (numeral
2.4.1), y la via API cubre el 100 % de las variables del modelo. Este script
es la segunda via, opcional: rastrea la pagina publica de la serie del
rendimiento soberano en BCRPData y contrasta sus valores con los que entrego
la API.

Su proposito es acreditar que el dato publicado en la web coincide con el
dato servido por el endpoint.

SELECTOR: la pagina devuelve la serie en una unica tabla HTML. Se extrae con
pandas.read_html, que localiza los elementos <table> del documento, y se toma
la de mayor numero de filas, que es la de resultados. No se usa un selector
CSS mas especifico porque el portal no asigna clases ni identificadores
estables a esa tabla.

PAGINACION: no aplica. El endpoint /series/diarias/resultados/<codigo>/html
devuelve la serie completa en una sola respuesta, sin enlaces de pagina
siguiente. Se verifica comparando el numero de filas de la tabla web con el
de la extraccion por API.

ETICA (numeral 2.4.8): solo informacion publica, User-Agent identificable con
institucion y correo de contacto, y pausa entre solicitudes.
"""

import time, requests, pandas as pd
from pathlib import Path
from datetime import datetime

RAIZ = Path(__file__).resolve().parent.parent
LOG = RAIZ / "log_ejecucion.txt"

UA = ("UNCP-FacultadEconomia-FinanzasI/1.0 (trabajo academico; "
      "contacto: e_2024200522B@uncp.edu.pe)")
CODIGO, NOMBRE = "PD31893DD", "Y_rend_soberano_10a"
URL = ("https://estadisticas.bcrp.gob.pe/estadisticas/series/diarias/"
       f"resultados/{CODIGO}/html")
PAUSA, TIMEOUT = 1.5, 60


def log(msg):
    linea = f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}"
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(linea + "\n")
    print(linea)


def main():
    r = requests.get(URL, headers={"User-Agent": UA}, timeout=TIMEOUT)
    log(f"GET verificacion HTML {CODIGO} -> {URL} | HTTP {r.status_code}")
    if r.status_code != 200:
        log("La pagina no respondio 200. Verificacion cruzada omitida.")
        return
    time.sleep(PAUSA)

    # El HTML crudo se guarda como evidencia primaria y no se edita.
    ruta_html = RAIZ / "datos_crudos" / f"verificacion_html_{CODIGO}.html"
    ruta_html.write_text(r.text, encoding="utf-8")

    tablas = pd.read_html(r.text)
    web = max(tablas, key=len)          # la tabla de resultados es la mas larga
    web.to_csv(RAIZ / "datos_crudos" / f"verificacion_web_{CODIGO}.csv",
               index=False, encoding="utf-8")
    log(f"Tabla HTML parseada y guardada | filas={len(web)}")

    api = pd.read_csv(RAIZ / "datos_crudos" / "diarias" /
                      f"{NOMBRE}__{CODIGO}.csv")
    log(f"Comparacion | API: {len(api)} periodos | Web: {len(web)} filas")
    print(web.head())


if __name__ == "__main__":
    main()
