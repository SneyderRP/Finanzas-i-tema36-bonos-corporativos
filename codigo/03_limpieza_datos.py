# Meglinho Sneyder Rojas Poma
# Codigo de matricula: 2024200522B
# Tema 36 del temario: Bonos corporativos en el mercado peruano: colocaciones, tasas y plazos
# Fecha de extraccion: 2026-09-25

"""
LIMPIEZA Y CONSTRUCCION DE LA SERIE DE TIEMPO DIARIA.

Entra:  datos_crudos_diario_<codigo>.csv   (3 913 dias, 5 series)
Sale:   datos_procesados_diario_<codigo>.csv
        datos_procesados_<codigo>.csv      (base del articulo)

Criterio de limpieza: NO se rellena ningun hueco. Se conservan unicamente los
dias en que las cinco series publicaron dato. Asi cada celda del archivo final
existe en la fuente oficial y resiste el cotejo del numeral 2.4.6.

Rellenar feriados con el ultimo valor conocido habria conservado mas filas,
pero habria producido celdas sin respaldo en la fuente para esa fecha.
"""

import hashlib
import pandas as pd
from pathlib import Path
from datetime import datetime

RAIZ = Path(__file__).resolve().parent.parent
LOG = RAIZ / "log_ejecucion.txt"

VARS = ["Y_rend_soberano_10a", "X1_tasa_referencia", "X2_treasury_10a",
        "X3_embig_peru", "X4_interbancaria"]


def log(msg):
    linea = f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}"
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(linea + "\n")
    print(linea)


def marcar_outliers(s, f=3.0):
    """Marca extremos por rango intercuartilico. NO los elimina: los senala."""
    q1, q3 = s.quantile(.25), s.quantile(.75)
    return (s < q1 - f * (q3 - q1)) | (s > q3 + f * (q3 - q1))


def main():
    crudo = RAIZ / "datos_crudos" / "datos_crudos_diario_2024200522B.csv"
    d = pd.read_csv(crudo, parse_dates=["fecha"])
    log(f"Leido crudo diario | filas={len(d)}")

    for c in VARS:
        log(f"Faltantes en {c}: {int(d[c].isna().sum())}")

    antes = len(d)
    d = d.dropna(subset=VARS).copy()
    log(f"Dias descartados por falta de publicacion: {antes - len(d)}")

    # El EMBIG viene en puntos basicos; las demas series en porcentaje.
    d["X3_riesgo_pais"] = d["X3_embig_peru"] / 100

    d["spread_soberano"] = d["Y_rend_soberano_10a"] - d["X2_treasury_10a"]
    d["anio"] = d.fecha.dt.year
    d["id"] = range(1, len(d) + 1)
    d["outlier_Y"] = marcar_outliers(d["Y_rend_soberano_10a"])

    cols = ["id", "fecha", "anio", "Y_rend_soberano_10a", "X1_tasa_referencia",
            "X2_treasury_10a", "X3_embig_peru", "X3_riesgo_pais",
            "X4_interbancaria", "spread_soberano", "outlier_Y"]
    proc = RAIZ / "datos_procesados" / "intermedio_diario_2024200522B.csv"
    d[cols].to_csv(proc, index=False, encoding="utf-8")
    log(f"Guardado procesado | filas={len(d)}")

    # ------------------------------------------------------------------
    # Tabla final: niveles mas variaciones diarias.
    # La prueba ADF mostro raiz unitaria en niveles para cuatro de las cinco
    # series, por lo que el modelo se estima sobre las variaciones.
    # ------------------------------------------------------------------
    t = pd.DataFrame({
        "id": range(1, len(d) + 1),
        "fecha": d["fecha"].dt.strftime("%Y-%m-%d"),
        "anio": d["fecha"].dt.year,
        "Y_rendimiento_soberano": d["Y_rend_soberano_10a"].values,
        "X1_tasa_referencia":     d["X1_tasa_referencia"].values,
        "X2_treasury_10a":        d["X2_treasury_10a"].values,
        "X3_riesgo_pais":         d["X3_riesgo_pais"].values,
        "X4_tasa_interbancaria":  d["X4_interbancaria"].values,
    })
    # La tabla final entrega los NIVELES de las cinco variables sustantivas.
    # Las variaciones diarias, que son las que entran al modelo por el
    # resultado del ADF, las calcula 04_analisis.py a partir de estos niveles.

    # La tabla final entrega id, fecha y las cinco variables sustantivas.
    t = t[["id", "fecha", "Y_rendimiento_soberano", "X1_tasa_referencia",
           "X2_treasury_10a", "X3_riesgo_pais", "X4_tasa_interbancaria"]]

    final = RAIZ / "datos_procesados" / "datos_procesados_2024200522B.csv"
    t.to_csv(final, index=False, encoding="utf-8")

    firma = hashlib.sha256(final.read_bytes()).hexdigest()
    log(f"Tabla final | filas={len(t)} | SHA-256: {firma}")

    print("\n" + "=" * 66)
    print("HASH DE LA TABLA FINAL (va al README):")
    print(firma)
    print("=" * 66)
    print(f"Filas: {len(t)} | Columnas: {len(t.columns)}")


if __name__ == "__main__":
    main()
