# Meglinho Sneyder Rojas Poma
# Codigo de matricula: 2024200522B
# Tema 36 del temario: Bonos corporativos en el mercado peruano: colocaciones, tasas y plazos
# Fecha de extraccion: 2026-09-26

"""
GRAFICOS COMPARATIVOS. Confronta la variable endogena con cada explicativa.

Genera cinco figuras adicionales a las de 04_analisis.py:

  figura5_Y_vs_X1.png   rendimiento soberano frente a tasa de referencia
  figura6_Y_vs_X2.png   rendimiento soberano frente a Treasury 10 anos
  figura7_Y_vs_X3.png   rendimiento soberano frente a riesgo pais
  figura8_Y_vs_X4.png   rendimiento soberano frente a tasa interbancaria
  figura9_matriz_correlaciones.png   matriz de correlaciones

Cada figura de comparacion tiene dos paneles:

  Panel superior  NIVELES. Ambas series en el tiempo. Muestra si se mueven
                  juntas a lo largo de los 15 anos.
  Panel inferior  VARIACIONES DIARIAS. Dispersion con recta ajustada. Es la
                  relacion que efectivamente estima el modelo, dado que la
                  prueba ADF mostro raiz unitaria en niveles.

La distincion importa: en niveles casi todo parece correlacionado porque las
series comparten tendencia. La dispersion en variaciones muestra la relacion
real, libre de ese efecto.
"""

import matplotlib
matplotlib.use("Agg")                # backend sin ventana
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime

RAIZ = Path(__file__).resolve().parent.parent
SAL = RAIZ / "salidas"
SAL.mkdir(exist_ok=True)
LOG = RAIZ / "log_ejecucion.txt"

Y = "Y_rendimiento_soberano"

# Cada explicativa con su etiqueta, su color y el coeficiente estimado
EXPL = {
    "X1_tasa_referencia":   ("Tasa de referencia del BCRP",      "#C0392B", "figura5_Y_vs_X1"),
    "X2_treasury_10a":      ("Bonos del Tesoro EE.UU. a 10 años", "#1F618D", "figura6_Y_vs_X2"),
    "X3_riesgo_pais":       ("Riesgo país (EMBIG Perú)",          "#B7950B", "figura7_Y_vs_X3"),
    "X4_tasa_interbancaria":("Tasa interbancaria en soles",       "#117A65", "figura8_Y_vs_X4"),
}

ETIQ_Y = "Rendimiento del bono peruano a 10 años"


def log(msg):
    linea = f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}"
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(linea + "\n")
    print(linea)


def comparar(d, var, etiqueta, color, nombre):
    """Dos paneles: niveles en el tiempo y dispersion en variaciones."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8.5))

    # --- Panel superior: niveles
    ax1.plot(d.fecha, d[Y], color="#2C3E50", linewidth=.9, label=ETIQ_Y)
    ax1.plot(d.fecha, d[var], color=color, linewidth=.9, label=etiqueta)
    ax1.set_xlabel("Fecha")
    ax1.set_ylabel("Porcentaje anual")
    ax1.set_title(f"Niveles: {ETIQ_Y} y {etiqueta}", fontsize=11)
    ax1.legend(fontsize=8)
    ax1.grid(alpha=.3)

    # Correlacion en niveles, informativa: las series comparten tendencia
    r_niv = d[[Y, var]].corr().iloc[0, 1]
    ax1.text(.02, .95, f"Correlación en niveles: {r_niv:.3f}",
             transform=ax1.transAxes, fontsize=9, va="top",
             bbox=dict(boxstyle="round", facecolor="white", alpha=.75))

    # --- Panel inferior: variaciones diarias
    dy = d[Y].diff()
    dx = d[var].diff()
    m = pd.concat([dx, dy], axis=1).dropna()

    ax2.scatter(m.iloc[:, 0], m.iloc[:, 1], s=7, alpha=.35, color=color)

    # Recta ajustada por minimos cuadrados sobre las variaciones
    b, a = np.polyfit(m.iloc[:, 0], m.iloc[:, 1], 1)
    eje = np.linspace(m.iloc[:, 0].min(), m.iloc[:, 0].max(), 100)
    ax2.plot(eje, a + b * eje, color="#2C3E50", linewidth=1.8)

    r_var = m.corr().iloc[0, 1]
    ax2.set_xlabel(f"Variación diaria de {etiqueta} (p.p.)")
    ax2.set_ylabel("Variación diaria del rendimiento (p.p.)")
    ax2.set_title(f"Variaciones diarias: pendiente = {b:.3f}", fontsize=11)
    ax2.grid(alpha=.3)
    ax2.axhline(0, color="gray", linewidth=.5)
    ax2.axvline(0, color="gray", linewidth=.5)
    ax2.text(.02, .95, f"Correlación en variaciones: {r_var:.3f}",
             transform=ax2.transAxes, fontsize=9, va="top",
             bbox=dict(boxstyle="round", facecolor="white", alpha=.75))

    plt.tight_layout()
    plt.savefig(SAL / f"{nombre}.png", dpi=300)
    plt.close()
    log(f"Salida generada: {nombre}.png | r_niveles={r_niv:.3f} r_variaciones={r_var:.3f}")
    return r_niv, r_var


def matriz(d):
    """Matriz de correlaciones en variaciones diarias."""
    cols = [Y] + list(EXPL)
    etiquetas = ["Y rendimiento", "X1 referencia", "X2 Treasury",
                 "X3 riesgo país", "X4 interbancaria"]
    c = d[cols].diff().corr()

    fig, ax = plt.subplots(figsize=(7.5, 6.5))
    im = ax.imshow(c, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(cols)))
    ax.set_yticks(range(len(cols)))
    ax.set_xticklabels(etiquetas, rotation=40, ha="right", fontsize=9)
    ax.set_yticklabels(etiquetas, fontsize=9)

    for i in range(len(cols)):
        for j in range(len(cols)):
            v = c.iloc[i, j]
            ax.text(j, i, f"{v:.3f}", ha="center", va="center", fontsize=9,
                    color="white" if abs(v) > .5 else "black")

    ax.set_title("Matriz de correlaciones en variaciones diarias", fontsize=11)
    fig.colorbar(im, ax=ax, shrink=.8)
    plt.tight_layout()
    plt.savefig(SAL / "figura9_matriz_correlaciones.png", dpi=300)
    plt.close()
    log("Salida generada: figura9_matriz_correlaciones.png")

    # Tambien se guarda como tabla, para insertarla en LaTeX
    c.index = etiquetas
    c.columns = etiquetas
    c.round(4).to_csv(SAL / "tabla5_correlaciones.csv", encoding="utf-8")
    (SAL / "tabla5_correlaciones.tex").write_text(
        c.round(4).to_latex(caption="Matriz de correlaciones en variaciones diarias",
                            label="tab:correlaciones"), encoding="utf-8")
    log("Salida generada: tabla5_correlaciones")


def main():
    d = pd.read_csv(RAIZ / "datos_procesados" / "datos_procesados_2024200522B.csv",
                    parse_dates=["fecha"])
    log(f"Graficos comparativos: base cargada | filas={len(d)}")

    resumen = []
    for var, (etiqueta, color, nombre) in EXPL.items():
        rn, rv = comparar(d, var, etiqueta, color, nombre)
        resumen.append({"Variable": etiqueta,
                        "Corr. en niveles": round(rn, 4),
                        "Corr. en variaciones": round(rv, 4)})

    matriz(d)

    t = pd.DataFrame(resumen).set_index("Variable")
    t.to_csv(SAL / "tabla6_correlaciones_con_Y.csv", encoding="utf-8")
    (SAL / "tabla6_correlaciones_con_Y.tex").write_text(
        t.to_latex(caption="Correlación de cada explicativa con la variable dependiente",
                   label="tab:corr_Y"), encoding="utf-8")
    log("Salida generada: tabla6_correlaciones_con_Y")

    print("\n" + t.to_string())
    print("\nNueve figuras y seis tablas disponibles en /salidas.")


if __name__ == "__main__":
    main()
