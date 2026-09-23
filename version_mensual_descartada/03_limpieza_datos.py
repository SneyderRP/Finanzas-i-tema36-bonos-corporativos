# Meglinho Sneyder Rojas Poma
# Codigo de matricula: 2024200522B
# Tema 36 del temario: Bonos corporativos en el mercado peruano: colocaciones, tasas y plazos
# Fecha de extraccion: 2026-09-23

"""
LIMPIEZA Y CONSTRUCCION DEL PANEL.

Entra:  datos_crudos_api_<codigo>.csv   (ancho: una fila por mes)
Sale:   datos_procesados_<codigo>.csv   (largo: una fila por instrumento y mes)

Por que formato largo: el articulo estudia siete instrumentos a lo largo del
tiempo. En ancho serian 180 filas; en largo son 7 x 180 = 1 260 observaciones,
que es un panel y permite estimar efectos fijos por instrumento.

Llave del panel: instrumento + fecha.
"""
import numpy as np, pandas as pd
from utilidades import cfg, registrar, hash_sha256

INSTRUMENTOS = {
    "coloc_sector_privado":  ("Sector privado (total)",   "Agregado",     "Colocacion"),
    "coloc_corporativos":    ("Bonos corporativos",       "Corporativo",  "Colocacion"),
    "coloc_arrendamiento":   ("Arrendamiento financiero", "Financiero",   "Colocacion"),
    "coloc_titulizacion":    ("Bonos de titulizacion",    "Titulizacion", "Colocacion"),
    "saldo_corporativos":    ("Saldo corporativos",       "Corporativo",  "Saldo"),
    "saldo_plazo_hasta_3a":  ("Saldo plazo hasta 3 anos", "Plazo corto",  "Saldo"),
    "saldo_plazo_3a_5a":     ("Saldo plazo 3 a 5 anos",   "Plazo medio",  "Saldo"),
}
MACRO = ["tasa_referencia", "rend_soberano_10a_pen", "rend_soberano_10a_usd",
         "embig_peru", "tasa_pref_corp_90d_mn", "tasa_corp_mas360_mn"]

def outliers(s, f=3.0):
    """Marca extremos por rango intercuartilico. NO los borra: los senala."""
    q1, q3 = s.quantile(.25), s.quantile(.75)
    return (s < q1 - f * (q3 - q1)) | (s > q3 + f * (q3 - q1))

def main():
    ancho = pd.read_csv(cfg.ARCHIVO_CRUDO, parse_dates=["fecha"])
    registrar("Leido crudo de la API", filas=len(ancho))

    faltan = [c for c in list(INSTRUMENTOS) + MACRO if c not in ancho.columns]
    if faltan:
        raise SystemExit("Faltan columnas en el crudo: " + ", ".join(faltan))

    # De ancho a largo: se apilan los siete instrumentos.
    p = ancho.melt(id_vars=["fecha"] + MACRO, value_vars=list(INSTRUMENTOS),
                   var_name="instrumento", value_name="monto_mill_soles")

    p["etiqueta"]  = p.instrumento.map(lambda c: INSTRUMENTOS[c][0])
    p["tipo_bono"] = p.instrumento.map(lambda c: INSTRUMENTOS[c][1])
    p["medida"]    = p.instrumento.map(lambda c: INSTRUMENTOS[c][2])
    p["anio"]      = p.fecha.dt.year
    p["mes_num"]   = p.fecha.dt.month

    # log1p y no log: hay meses sin colocacion, con valor cero, y log(0) no existe.
    p["log_monto"]       = np.log1p(p.monto_mill_soles.clip(lower=0))
    # Prima por plazo: cuanto mas paga el soberano a 10 anos que la tasa de politica.
    p["prima_plazo"]     = p.rend_soberano_10a_pen - p.tasa_referencia
    # Spread bancario: costo del credito por encima de la tasa de politica.
    p["spread_bancario"] = p.tasa_pref_corp_90d_mn - p.tasa_referencia
    # EMBIG viene en puntos basicos; se pasa a porcentaje para compararlo con tasas.
    p["riesgo_pais_pct"] = p.embig_peru / 100
    p["outlier_monto"]   = p.groupby("instrumento").monto_mill_soles.transform(outliers)

    cols = ["fecha","anio","mes_num","instrumento","etiqueta","tipo_bono","medida",
            "monto_mill_soles","log_monto","tasa_referencia","rend_soberano_10a_pen",
            "rend_soberano_10a_usd","embig_peru","riesgo_pais_pct",
            "tasa_pref_corp_90d_mn","tasa_corp_mas360_mn",
            "prima_plazo","spread_bancario","outlier_monto"]
    p = p[cols].sort_values(["instrumento", "fecha"])
    p.to_csv(cfg.ARCHIVO_PROCESADO, index=False, encoding="utf-8")

    firma = hash_sha256(cfg.ARCHIVO_PROCESADO)
    registrar(f"Panel construido {cfg.ARCHIVO_PROCESADO.name}", filas=len(p))
    registrar(f"SHA-256 del procesado: {firma}")

    print("\n" + "=" * 66)
    print("PEGA ESTE HASH EN EL README.md:"); print(firma)
    print("=" * 66)
    print(f"Observaciones : {len(p)}   (minimo 1 000)")
    print(f"Columnas      : {len(p.columns)}   (minimo 6)")
    print(f"Instrumentos  : {p.instrumento.nunique()}")
    print(f"Periodos      : {p.fecha.nunique()} meses   (minimo 60)")

if __name__ == "__main__":
    main()
