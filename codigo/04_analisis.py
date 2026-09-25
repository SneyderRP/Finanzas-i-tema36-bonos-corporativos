# Meglinho Sneyder Rojas Poma
# Codigo de matricula: 2024200522B
# Tema 36 del temario: Bonos corporativos en el mercado peruano: colocaciones, tasas y plazos
# Fecha de extraccion: 2026-09-25

"""
ANALISIS. Genera TODAS las tablas y figuras del articulo.

Criterio 4: cada tabla y figura debe regenerarse con este archivo.

Secuencia:
  1. Descriptiva de las cinco series
  2. Prueba de raiz unitaria (Dickey-Fuller aumentada)
  3. Regresion en niveles -> diagnostico, resulta espuria
  4. Regresion en variaciones diarias -> modelo principal
  5. Figuras

Por que el modelo va en variaciones: el ADF no rechaza raiz unitaria en
niveles para cuatro de las cinco series, y la regresion en niveles arroja
Durbin-Watson de 0.038, muy lejos del 2 esperado. Es el patron clasico de
regresion espuria. Al diferenciar, el Durbin-Watson sube a 2.087.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.tsa.stattools import adfuller
from pathlib import Path
from datetime import datetime

RAIZ = Path(__file__).resolve().parent.parent
SAL = RAIZ / "salidas"; SAL.mkdir(exist_ok=True)
LOG = RAIZ / "log_ejecucion.txt"

NIV = ["Y_rendimiento_soberano", "X1_tasa_referencia", "X2_treasury_10a",
       "X3_riesgo_pais", "X4_tasa_interbancaria"]
DIF = ["d_" + v for v in NIV]

ETIQ = {"Y_rendimiento_soberano": "Rendimiento del bono peruano a 10 anos",
        "X1_tasa_referencia":     "Tasa de referencia del BCRP",
        "X2_treasury_10a":        "Bonos del Tesoro EE.UU. a 10 anos",
        "X3_riesgo_pais":         "Riesgo pais (EMBIG Peru)",
        "X4_tasa_interbancaria":  "Tasa interbancaria en soles"}


def log(msg):
    linea = f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}"
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(linea + "\n")
    print(linea)


def guardar(t, nombre, titulo):
    t.to_csv(SAL / f"{nombre}.csv", encoding="utf-8")
    (SAL / f"{nombre}.tex").write_text(
        t.to_latex(caption=titulo, label=f"tab:{nombre}", float_format="%.4f"),
        encoding="utf-8")
    log(f"Salida generada: {nombre}")


def figura(nombre):
    plt.tight_layout()
    plt.savefig(SAL / f"{nombre}.png", dpi=300)
    plt.close()
    log(f"Salida generada: {nombre}.png")


def main():
    d = pd.read_csv(RAIZ / "datos_procesados" / "tabla_final_2024200522B.csv",
                    parse_dates=["fecha"])
    log(f"Analisis: tabla final cargada | filas={len(d)}")

    # La tabla final entrega solo niveles. Las variaciones diarias se calculan
    # aqui: el ADF mostro raiz unitaria en niveles para cuatro de las cinco
    # series, por lo que el modelo principal se estima sobre las variaciones.
    for v in NIV:
        d["d_" + v] = d[v].diff()

    # --- Tabla 1: descriptiva
    t1 = d[NIV].describe().T[["count", "mean", "std", "min", "50%", "max"]]
    t1.columns = ["N", "Media", "Desv. tip.", "Minimo", "Mediana", "Maximo"]
    t1.index = [ETIQ[i] for i in t1.index]
    guardar(t1, "tabla1_descriptiva", "Estadistica descriptiva de las series diarias")

    # --- Tabla 2: raiz unitaria
    filas = []
    for v in NIV:
        pn = adfuller(d[v].dropna(), autolag="AIC")[1]
        pd_ = adfuller(d[v].diff().dropna(), autolag="AIC")[1]
        filas.append({"Variable": ETIQ[v], "p-valor en nivel": round(pn, 4),
                      "p-valor en variacion": round(pd_, 4),
                      "Orden": "I(0)" if pn < 0.05 else "I(1)"})
    guardar(pd.DataFrame(filas).set_index("Variable"), "tabla2_adf",
            "Prueba de raiz unitaria de Dickey-Fuller aumentada")

    # --- Tabla 3: niveles (diagnostico)
    m1 = smf.ols("Y_rendimiento_soberano ~ " + " + ".join(NIV[1:]),
                 data=d).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
    dw1 = sm.stats.durbin_watson(m1.resid)
    guardar(pd.DataFrame({"Coeficiente": m1.params, "Error estandar": m1.bse,
                          "z": m1.tvalues, "p-valor": m1.pvalues}),
            "tabla3_niveles", "Regresion en niveles (diagnostico de espuriedad)")
    (SAL / "tabla3_completa.txt").write_text(str(m1.summary()), encoding="utf-8")
    log(f"Niveles | R2={m1.rsquared:.3f} | Durbin-Watson={dw1:.3f}")

    # --- Tabla 4: variaciones (modelo principal)
    dd = d.dropna(subset=DIF)
    m2 = smf.ols("d_Y_rendimiento_soberano ~ " + " + ".join(DIF[1:]),
                 data=dd).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
    dw2 = sm.stats.durbin_watson(m2.resid)
    guardar(pd.DataFrame({"Coeficiente": m2.params, "Error estandar": m2.bse,
                          "z": m2.tvalues, "p-valor": m2.pvalues}),
            "tabla4_variaciones",
            "Determinantes de las variaciones diarias del rendimiento soberano")
    (SAL / "tabla4_completa.txt").write_text(str(m2.summary()), encoding="utf-8")
    log(f"Variaciones | R2={m2.rsquared:.3f} | Durbin-Watson={dw2:.3f} | N={int(m2.nobs)}")

    # --- Figura 1: las cuatro tasas
    plt.figure(figsize=(11, 5))
    for v in ["Y_rendimiento_soberano", "X1_tasa_referencia",
              "X2_treasury_10a", "X3_riesgo_pais"]:
        plt.plot(d.fecha, d[v], label=ETIQ[v], linewidth=.9)
    plt.xlabel("Fecha"); plt.ylabel("Porcentaje anual")
    plt.title("Rendimiento soberano peruano y sus determinantes, 2011-2025")
    plt.legend(fontsize=8); plt.grid(alpha=.3)
    figura("figura1_series_diarias")

    # --- Figura 2: spread sobre el Tesoro
    plt.figure(figsize=(11, 4))
    plt.plot(d.fecha, d.Y_rendimiento_soberano - d.X2_treasury_10a, linewidth=.9)
    plt.xlabel("Fecha"); plt.ylabel("Puntos porcentuales")
    plt.title("Spread del bono peruano sobre el Tesoro de EE.UU. a 10 anos")
    plt.grid(alpha=.3)
    figura("figura2_spread_soberano")

    # --- Figura 3: volatilidad de las variaciones
    plt.figure(figsize=(11, 4))
    plt.plot(dd.fecha, dd.d_Y_rendimiento_soberano, linewidth=.6)
    plt.xlabel("Fecha"); plt.ylabel("Variacion diaria (p.p.)")
    plt.title("Variaciones diarias del rendimiento soberano")
    plt.grid(alpha=.3)
    figura("figura3_variaciones")

    # --- Figura 4: dispersion frente al riesgo pais
    plt.figure(figsize=(6.5, 5))
    plt.scatter(dd.d_X3_riesgo_pais, dd.d_Y_rendimiento_soberano, s=6, alpha=.4)
    plt.xlabel("Variacion diaria del riesgo pais (p.p.)")
    plt.ylabel("Variacion diaria del rendimiento (p.p.)")
    plt.title("Riesgo pais y rendimiento soberano")
    plt.grid(alpha=.3)
    figura("figura4_riesgo_vs_rendimiento")

    log("Analisis terminado.")
    print(f"\nNiveles      R2={m1.rsquared:.3f}  DW={dw1:.3f}  <- espuria")
    print(f"Variaciones  R2={m2.rsquared:.3f}  DW={dw2:.3f}  <- modelo principal")


if __name__ == "__main__":
    main()
