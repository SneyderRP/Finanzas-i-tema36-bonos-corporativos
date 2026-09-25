# Diccionario de variables

**Archivo:** `datos_procesados/datos_procesados_2024200522B.csv`
**Estudiante:** ROJAS POMA, MEGLINHO SNEYDER — 2024200522B
**Tema 36:** Bonos corporativos en el mercado peruano: colocaciones, tasas y plazos

**Estructura:** serie de tiempo diaria. Una fila = un día hábil.
**Observaciones:** 3692 · **Columnas:** 7 · **Ventana:** 2011-01-03 a 2025-12-31
**SHA-256:** `4a337051ed234cb00947c3c6fea7be9d284e216c713ca701ed43e23847fe326f`

**Fuente única:** BCRPData, Banco Central de Reserva del Perú.
**Endpoint:** `https://estadisticas.bcrp.gob.pe/estadisticas/series/api/{código}/json/{inicio}/{fin}/esp`
**Acceso:** API REST pública, sin clave ni registro.

---

## Identificadores

| Variable | Definición | Tipo |
|---|---|---|
| `id` | Correlativo de 1 a 3692 | entero |
| `fecha` | Día hábil de observación | fecha AAAA-MM-DD |

## Variable dependiente

| Variable | Definición | Unidad | Código | Cobertura |
|---|---|---|---|---|
| `Y_rendimiento_soberano` | Rendimiento del bono del gobierno peruano a 10 años, en soles. Tasa base sobre la que se fija el costo de cualquier emisión corporativa local | % anual | `PD31893DD` | desde 13-05-2005 |

## Variables explicativas

| Variable | Definición | Unidad | Código | Cobertura |
|---|---|---|---|---|
| `X1_tasa_referencia` | Tasa de referencia de la política monetaria del BCRP | % anual | `PD12301MD` | desde 05-09-2003 |
| `X2_treasury_10a` | Rendimiento de los bonos del Tesoro de EE.UU. a 10 años. Tasa global libre de riesgo | % anual | `PD04719XD` | desde 14-01-1997 |
| `X3_riesgo_pais` | EMBIG Perú. Diferencial de rendimientos del índice de bonos de mercados emergentes, convertido de puntos básicos a porcentaje | % | `PD04709XD` | desde 01-01-1998 |
| `X4_tasa_interbancaria` | Tasa de interés interbancaria en soles | % anual | `PD04692MD` | desde 03-04-1995 |

**Cinco variables sustantivas.** El numeral 2.4.1 exige un mínimo de cuatro.

## Única transformación aplicada

`X3_riesgo_pais = PD04709XD / 100`

El EMBIG se publica en puntos básicos y las demás series en porcentaje. La
división hace que todas sean comparables en la misma unidad. Ninguna otra
variable se transforma: los cuatro restantes se entregan tal como los publica
la fuente.

## Tratamiento de datos faltantes

**No se rellenó ningún hueco.** De los 3 913 días del rango se conservan los
3692 en que las cinco series publicaron dato.

| Serie | Días sin publicación |
|---|---|
| `Y_rendimiento_soberano` | 186 |
| `X1_tasa_referencia` | 107 |
| `X2_treasury_10a` | 10 |
| `X3_riesgo_pais` | 0 |
| `X4_tasa_interbancaria` | 159 |

Total de días descartados: 221.

Los feriados no coinciden entre el mercado peruano y el estadounidense, y el
bono soberano no se negocia todos los días. Rellenar con el último valor
conocido habría conservado esas filas, pero habría producido celdas sin
respaldo en la fuente para esa fecha. Con el criterio adoptado, **cada celda
del archivo existe en BCRPData** y resiste el cotejo del numeral 2.4.6.

El archivo final no contiene ningún valor ausente.

## Variables calculadas en el análisis

`04_analisis.py` calcula las variaciones diarias (`d_` + nombre) a partir de
los niveles de esta tabla. No se almacenan aquí porque se derivan de las
columnas existentes.

La prueba de Dickey-Fuller aumentada no rechaza la hipótesis de raíz unitaria
en niveles para cuatro de las cinco series, por lo que el modelo principal se
estima sobre las variaciones diarias.

| Variable | p-valor en nivel | p-valor en variación | Orden |
|---|---|---|---|
| `Y_rendimiento_soberano` | 0,2128 | 0,0000 | I(1) |
| `X1_tasa_referencia` | 0,4749 | 0,0000 | I(1) |
| `X2_treasury_10a` | 0,6533 | 0,0000 | I(1) |
| `X3_riesgo_pais` | 0,0003 | 0,0000 | I(0) |
| `X4_tasa_interbancaria` | 0,6058 | 0,0000 | I(1) |

## Sustituciones respecto del temario

El temario asigna al tema 36 seis variables y propone la SMV como vía 2. Dos de
ellas no existen como serie accesible por vía automatizada:

| Variable del temario | Situación | Sustituto |
|---|---|---|
| Tasa de colocación por emisión | No existe como serie. El SIMV de la SMV exige un token cifrado que se genera por sesión | `Y_rendimiento_soberano`: tasa base del mercado de bonos peruano |
| Clasificación de riesgo del emisor | La emiten clasificadoras privadas, no se publica como serie | `X3_riesgo_pais`: riesgo crediticio puesto en precio por el mercado |

El detalle de la exploración de fuentes está en `incidencias_fuente.md`.

## Verificación contra la fuente

Se cotejaron diez observaciones al azar contra la API en vivo, con coincidencia
en las diez. Los enlaces públicos de cada serie están en
`datos_crudos/verificacion_series_diarias.csv`.

## Citación en APA 7 (numeral 2.4.8)

Banco Central de Reserva del Perú. (2026). *BCRPData: base de datos
estadísticos* [Conjunto de datos]. Consultado el 2026-09-25.
https://estadisticas.bcrp.gob.pe/estadisticas/series/
