# Diccionario de variables

**Archivo:** `datos_procesados/datos_procesados_2024200522B.csv`
**Estudiante:** ROJAS POMA, MEGLINHO SNEYDER — 2024200522B
**Estructura:** panel. Una fila = un instrumento en un mes.
**Llave:** `instrumento` + `fecha` · **Ventana:** 2011-01 a 2025-12 (180 meses × 7 = 1260 obs.)
**Fuente única:** BCRPData, Banco Central de Reserva del Perú. API REST pública, sin clave.
**Endpoint:** `https://estadisticas.bcrp.gob.pe/estadisticas/series/api/{código}/json/{inicio}/{fin}/esp`

## Identificadores

| Variable | Definición | Tipo |
|---|---|---|
| `fecha` | Primer día del mes de observación | fecha |
| `anio`, `mes_num` | Año y mes, derivados de `fecha` | entero |
| `instrumento` | Código del instrumento. Con `fecha` forma la llave | texto |
| `etiqueta` | Nombre legible, para tablas y figuras | texto |
| `tipo_bono` | Agregado, Corporativo, Financiero, Titulización, Plazo corto, Plazo medio | categórica |
| `medida` | Flujo (Colocación) o stock (Saldo) | categórica |

## Dependiente

| Variable | Definición | Unidad |
|---|---|---|
| `monto_mill_soles` | Monto del instrumento en el mes | millones de S/ |
| `log_monto` | `ln(1 + monto)`. **Dependiente del modelo.** Se usa `log1p` porque hay meses sin colocación, con valor cero, y `log(0)` no existe | adimensional |

### Las siete series del panel (cuadros cn-058 y cn-059 de la Nota Semanal)

| `instrumento` | Código | Serie oficial |
|---|---|---|
| `coloc_sector_privado` | `PN01064MM` | Bonos · Sector Privado · Colocación |
| `coloc_corporativos` | `PN01081MM` | Entidades No Financieras · Bonos Corporativos · Colocación |
| `coloc_arrendamiento` | `PN01068MM` | Entidades Financieras · Arrendamiento Financiero · Colocación |
| `coloc_titulizacion` | `PN01084MM` | Entidades No Financieras · Bonos de Titulización · Colocación |
| `saldo_corporativos` | `PN01101MM` | Saldos · Por Tipo · Corporativos |
| `saldo_plazo_hasta_3a` | `PN01103MM` | Saldos · Por Plazo · Hasta 3 años |
| `saldo_plazo_3a_5a` | `PN01104MM` | Saldos · Por Plazo · De 3 hasta 5 años |

## Explicativas

Comunes a todos los instrumentos del mismo mes, como corresponde en un panel.

| Variable | Código | Definición | Unidad | Cobertura |
|---|---|---|---|---|
| `tasa_referencia` | `PD04722MM` | Tasa de Referencia de la Política Monetaria | % anual | Sep-2003 → Ago-2026 |
| `rend_soberano_10a_pen` | `PD31895MM` | Rendimiento del bono peruano a 10 años, soles | % anual | May-2005 → Ago-2026 |
| `rend_soberano_10a_usd` | `PD31896MM` | Rendimiento del bono peruano a 10 años, dólares | % anual | Jul-2009 → Ago-2026 |
| `embig_peru` | `PN01129XM` | EMBIG Perú. Diferencial de rendimientos del índice de bonos de mercados emergentes | puntos básicos | Ago-2006 → Jun-2026 |
| `tasa_pref_corp_90d_mn` | `PN07809NM` | Tasa activa preferencial corporativa a 90 días, MN | % anual | Ago-2010 → Ago-2026 |
| `tasa_corp_mas360_mn` | `PN07842NM` | Tasa activa a corporativos, grandes y medianas, préstamos > 360 días, MN | % anual | Ago-2010 → Ago-2026 |

## Construidas por `03_limpieza_datos.py`

| Variable | Definición | Cálculo |
|---|---|---|
| `riesgo_pais_pct` | EMBIG en porcentaje, comparable con las demás tasas | `embig_peru / 100` |
| `prima_plazo` | Cuánto más paga el soberano a 10 años que la tasa de política | `rend_soberano_10a_pen − tasa_referencia` |
| `spread_bancario` | Sobrecosto del crédito bancario corporativo sobre la tasa de política. Comparador del bono frente al préstamo | `tasa_pref_corp_90d_mn − tasa_referencia` |
| `outlier_monto` | Marca extremos dentro de cada instrumento, por rango intercuartílico con factor 3. No se eliminan: se señalan | `monto < Q1 − 3·RIC` o `monto > Q3 + 3·RIC` |

## Sustituciones respecto del temario

El temario pedía **tasa de colocación** y **clasificación de riesgo**. Ninguna
existe como serie en BCRPData: se revisaron las 209 series mensuales de la
categoría Tasas de interés y los cuadros de bonos.

- **Tasa de colocación** → la dependiente pasa a ser el monto colocado, y
  `spread_bancario` entra como medida del costo de financiamiento alternativo.
- **Clasificación de riesgo** → `embig_peru`, riesgo crediticio puesto en precio
  por el mercado en lugar de calificado por una agencia.

Ambas sustituciones se declaran en la sección de Materiales y métodos del artículo.

## Notas de tratamiento

- Los valores marcados `n.d.` por el BCRP se convierten en vacío. **Nunca se
  rellenan con un valor inventado.**
- El monto cero es dato real: significa que ese mes no hubo colocación de ese
  instrumento. Por eso se usa `log1p`.
- Los datos crudos de `/datos_crudos` se entregan tal como salieron de la API.
  No se editan bajo ninguna circunstancia (numeral 2.4.5).

## Citación en APA 7

Banco Central de Reserva del Perú. (2026). *BCRPData: base de datos estadísticos*
[Conjunto de datos]. Consultado el 2026-09-22.
https://estadisticas.bcrp.gob.pe/estadisticas/series/
