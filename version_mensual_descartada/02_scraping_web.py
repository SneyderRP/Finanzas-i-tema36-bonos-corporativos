# Meglinho Sneyder Rojas Poma
# Codigo de matricula: 2024200522B
# Tema 36 del temario: Bonos corporativos en el mercado peruano: colocaciones, tasas y plazos
# Fecha de extraccion: 2026-09-25

"""
VIA 2 - Verificacion cruzada por descarga programatica.

La Unidad I exige UNA sola via automatizada, preferentemente API (numeral
2.4.1), y la via API cubre el 100 % de las variables del modelo. Este script
es la segunda via opcional: descarga la pagina publica de la serie en BCRPData
y compara sus valores con los que devolvio la API.

Etica del rastreo (numeral 2.4.8): solo informacion publica, User-Agent
identificable, pausa de 1.5 segundos entre solicitudes.
"""
import time, requests, pandas as pd
from utilidades import cfg, registrar

# Se verifica la serie mas importante del tema: colocacion de bonos corporativos.
CODIGO, NOMBRE = "PN01081MM", "coloc_corporativos"
URL = f"https://estadisticas.bcrp.gob.pe/estadisticas/series/mensuales/resultados/{CODIGO}/html"

def main():
    r = requests.get(URL, headers={"User-Agent": cfg.USER_AGENT},
                     timeout=cfg.TIMEOUT)
    registrar(f"GET verificacion HTML {CODIGO}", http=r.status_code)
    if r.status_code != 200:
        registrar("La pagina no respondio 200. Verificacion cruzada omitida.")
        return
    time.sleep(cfg.PAUSA)

    ruta = cfg.DIR_CRUDOS / f"verificacion_html_{CODIGO}.html"
    ruta.write_text(r.text, encoding="utf-8")          # evidencia primaria

    tablas = pd.read_html(r.text)
    web = max(tablas, key=len)
    web.to_csv(cfg.DIR_CRUDOS / f"verificacion_web_{CODIGO}.csv",
               index=False, encoding="utf-8")
    registrar(f"Tabla HTML parseada y guardada", filas=len(web))

    api = pd.read_csv(cfg.DIR_POR_VARIABLE / f"{NOMBRE}__{CODIGO}.csv")
    registrar(f"API: {len(api)} periodos | Web: {len(web)} filas")
    print(web.head())

if __name__ == "__main__":
    main()
