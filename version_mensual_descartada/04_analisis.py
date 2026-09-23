# Meglinho Sneyder Rojas Poma
# Codigo de matricula: 2024200522B
# Tema 36 del temario: Bonos corporativos en el mercado peruano: colocaciones, tasas y plazos
# Fecha de extraccion: 2026-09-23

"""
ANALISIS DEL PANEL. Genera TODAS las tablas y figuras del articulo.

Criterio 4 de la rubrica: cada tabla y cada figura debe regenerarse con este
archivo. Una tabla que no se regenera se anula en el articulo.

Modelo: log_monto(i,t) = a(i) + b1*tasa_referencia + b2*prima_plazo
                         + b3*riesgo_pais_pct + b4*spread_bancario + e(i,t)

Los efectos fijos a(i) absorben lo que distingue a cada instrumento y no cambia
en el tiempo. Los coeficientes se leen como variacion DENTRO del instrumento.
Errores agrupados por instrumento: sus observaciones estan correlacionadas.
"""
import matplotlib
matplotlib.use("Agg")                 # backend sin ventana: corre en cualquier maquina
import matplotlib.pyplot as plt
import numpy as np, pandas as pd
import statsmodels.formula.api as smf
from utilidades import cfg, registrar

np.random.seed(cfg.SEMILLA)           # semilla del codigo de matricula (2.4.4)
EXPL = ["tasa_referencia", "prima_plazo", "riesgo_pais_pct", "spread_bancario"]

def guardar_tabla(t, nombre, titulo):
    t.to_csv(cfg.DIR_SALIDAS / f"{nombre}.csv", encoding="utf-8")
    (cfg.DIR_SALIDAS / f"{nombre}.tex").write_text(
        t.to_latex(caption=titulo, label=f"tab:{nombre}", float_format="%.3f"),
        encoding="utf-8")
    registrar(f"Salida generada: {nombre}")

def guardar_figura(nombre):
    plt.tight_layout()
    plt.savefig(cfg.DIR_SALIDAS / f"{nombre}.png", dpi=300)
    plt.close()
    registrar(f"Salida generada: {nombre}.png")

def main():
    p = pd.read_csv(cfg.ARCHIVO_PROCESADO, parse_dates=["fecha"])
    registrar("Analisis: panel cargado", filas=len(p))

    # Tabla 1 - descriptiva
    d = p[["monto_mill_soles", "log_monto"] + EXPL].describe().T
    d = d[["count","mean","std","min","50%","max"]]
    d.columns = ["N","Media","Desv. tip.","Minimo","Mediana","Maximo"]
    guardar_tabla(d, "tabla1_descriptiva", "Estadistica descriptiva del panel")

    # Tabla 2 - composicion del panel
    c = p.groupby("etiqueta").agg(observaciones=("monto_mill_soles","size"),
                                  promedio=("monto_mill_soles","mean"),
                                  mediana=("monto_mill_soles","median"),
                                  maximo=("monto_mill_soles","max"))
    guardar_tabla(c, "tabla2_por_instrumento", "Composicion del panel por instrumento")

    # Tabla 3 - panel con efectos fijos
    m = p.replace([np.inf,-np.inf], np.nan).dropna(subset=["log_monto"] + EXPL)
    mod = smf.ols("log_monto ~ " + " + ".join(EXPL) + " + C(instrumento)",
                  data=m).fit(cov_type="cluster",
                              cov_kwds={"groups": m["instrumento"]})
    fil = [v for v in mod.params.index if not v.startswith("C(instrumento)")]
    guardar_tabla(pd.DataFrame({"Coeficiente": mod.params[fil],
                                "Error estandar": mod.bse[fil],
                                "t": mod.tvalues[fil],
                                "p-valor": mod.pvalues[fil]}),
                  "tabla3_panel_efectos_fijos",
                  "Determinantes del monto colocado. Panel con efectos fijos")
    (cfg.DIR_SALIDAS / "tabla3_salida_completa.txt").write_text(
        str(mod.summary()), encoding="utf-8")
    registrar(f"Panel con efectos fijos estimado | N={int(mod.nobs)}")

    # Tabla 4 - robustez: solo bonos corporativos
    mc = p[p.instrumento == "coloc_corporativos"].dropna(subset=["log_monto"] + EXPL)
    m2 = smf.ols("log_monto ~ " + " + ".join(EXPL), data=mc).fit(cov_type="HC3")
    guardar_tabla(pd.DataFrame({"Coeficiente": m2.params, "Error estandar": m2.bse,
                                "t": m2.tvalues, "p-valor": m2.pvalues}),
                  "tabla4_robustez_corporativos",
                  "Robustez: colocacion de bonos corporativos solamente")

    # Figura 1 - colocacion anual por tipo
    p[p.medida == "Colocacion"].pivot_table(index="anio", columns="etiqueta",
        values="monto_mill_soles", aggfunc="sum").plot(kind="bar", stacked=True,
                                                       figsize=(10,5))
    plt.xlabel("Ano"); plt.ylabel("Colocacion (millones S/)")
    plt.title("Colocacion anual de bonos del sector privado")
    plt.legend(fontsize=8); plt.grid(axis="y", alpha=.3)
    guardar_figura("figura1_colocacion_anual")

    # Figura 2 - tasas y riesgo pais
    mac = p.drop_duplicates("fecha").set_index("fecha").sort_index()
    plt.figure(figsize=(10,5))
    for col, eti in [("tasa_referencia","Tasa de referencia"),
                     ("rend_soberano_10a_pen","Soberano 10 anos (S/)"),
                     ("tasa_pref_corp_90d_mn","Preferencial corporativa 90d"),
                     ("riesgo_pais_pct","EMBIG Peru (%)")]:
        plt.plot(mac.index, mac[col], label=eti)
    plt.xlabel("Mes"); plt.ylabel("Porcentaje anual")
    plt.title("Tasas de referencia, rendimiento soberano y riesgo pais")
    plt.legend(fontsize=8); plt.grid(alpha=.3)
    guardar_figura("figura2_tasas_y_riesgo")

    # Figura 3 - politica monetaria y colocacion corporativa
    mu = p[p.instrumento == "coloc_corporativos"].dropna(
        subset=["tasa_referencia","log_monto"])
    plt.figure(figsize=(7,5))
    plt.scatter(mu.tasa_referencia, mu.log_monto, s=14, alpha=.6)
    b, a = np.polyfit(mu.tasa_referencia, mu.log_monto, 1)
    ejes = np.linspace(mu.tasa_referencia.min(), mu.tasa_referencia.max(), 100)
    plt.plot(ejes, a + b*ejes, linewidth=2)
    plt.xlabel("Tasa de referencia (%)"); plt.ylabel("log(1 + monto colocado)")
    plt.title("Politica monetaria y colocacion de bonos corporativos")
    plt.grid(alpha=.3)
    guardar_figura("figura3_tasa_vs_colocacion")

    # Figura 4 - saldos por tramo de plazo
    p[p.instrumento.isin(["saldo_plazo_hasta_3a","saldo_plazo_3a_5a"])].pivot_table(
        index="fecha", columns="etiqueta", values="monto_mill_soles",
        aggfunc="mean").plot(figsize=(10,5))
    plt.xlabel("Mes"); plt.ylabel("Saldo (millones S/)")
    plt.title("Saldo vigente de bonos del sector privado por tramo de plazo")
    plt.legend(fontsize=8); plt.grid(alpha=.3)
    guardar_figura("figura4_saldos_por_plazo")

    registrar("Analisis terminado. Salidas en /salidas.")
    print(mod.summary())

if __name__ == "__main__":
    main()
