# Base de datos y código — Unidad I

**Estudiante:** ROJAS POMA, MEGLINHO SNEYDER
**Código de matrícula:** 2024200522B
**Curso:** Finanzas I (055D) · Escuela Profesional de Economía · UNCP · 2026-II
**Tema del temario:** N.º 36 — Bonos corporativos en el mercado peruano: colocaciones, tasas y plazos
**Docente:** Dr. Ciro Iván Machacuay Meza

## 1. Objetivo

Analizar los determinantes del rendimiento de los bonos del gobierno peruano a
10 años, tasa base sobre la que se fija el costo de cualquier emisión corporativa
local, a partir de la política monetaria doméstica, las condiciones financieras
globales y el riesgo país.

**Estructura:** serie de tiempo diaria, 2011-2025.
**Observaciones:** 3692 días hábiles con las cinco series publicadas.
**Dependiente:** variación diaria del rendimiento del bono peruano a 10 años.
**Explicativas:** tasa de referencia del BCRP, rendimiento del Tesoro de EE.UU.
a 10 años, riesgo país (EMBIG Perú) y tasa interbancaria en soles.

## 2. Fuente y endpoint

| Campo | Valor |
|---|---|
| Fuente | BCRPData, Banco Central de Reserva del Perú |
| Tipo | API REST pública, sin clave de acceso |
| Endpoint | `https://estadisticas.bcrp.gob.pe/estadisticas/series/api/{código}/json/{inicio}/{fin}/esp` |
| Series | 5, todas diarias. Ver `diccionario_variables.md` |
| Fecha de consulta | 2026-09-26 |

Cada serie se descarga por separado y se guarda en `datos_crudos/diarias/`, para
poder cotejarla contra la fuente oficial una por una (numeral 2.4.6).

**Vía 2.** El numeral 2.4.1 exige una sola vía automatizada en la Unidad I,
preferentemente API, y la vía API cubre el 100 % de las variables del modelo.
La exploración del portal de la SMV está documentada en `incidencias_fuente.md`.

## 3. Ventana congelada (numeral 2.4.5)

| Parámetro | Valor |
|---|---|
| `INICIO` | 2011-01-01 |
| `FIN` | 2025-12-31 |

Declarados como constantes en `codigo/01_extraccion_api.py`. Ningún script usa
la fecha del día.

## 4. Orden de ejecución

```bash
cd codigo
pip install -r ../requirements.txt

python 01_extraccion_api.py    # 5 series diarias   -> /datos_crudos
python 03_limpieza_datos.py    # limpieza y tabla   -> /datos_procesados
python 04_analisis.py          # tablas y figuras   -> /salidas
python 05_graficos_comparativos.py   # comparativos -> /salidas
```

## 5. Versiones

| Componente | Versión |
|---|---|
| Sistema operativo | Linux-6.6.122+-x86_64-with-glibc2.39 |
| Python | 3.13.15 |
| Librerías | ver `requirements.txt` |

## 6. Integridad del archivo procesado

| Campo | Valor |
|---|---|
| Archivo | `datos_procesados/datos_procesados_2024200522B.csv` |
| SHA-256 | `4a337051ed234cb00947c3c6fea7be9d284e216c713ca701ed43e23847fe326f` |
| Filas | 3692 |
| Columnas | 7 |

El hash se coteja contra el archivo entregado, nunca contra una reejecución
posterior (numeral 2.4.5).

## 7. Tratamiento de datos faltantes

**No se rellenó ningún hueco.** De los 3 913 días calendario del rango, se
conservan los 3692 en que las cinco series publicaron dato. Los 221
descartados corresponden a feriados y días sin negociación, distintos entre el
mercado peruano y el estadounidense.

Rellenar esos días con el último valor conocido habría conservado más
observaciones, pero habría producido celdas sin respaldo en la fuente para esa
fecha. Con el criterio adoptado, **cada celda del archivo final existe en
BCRPData** y resiste el cotejo del numeral 2.4.6.

## 8. Claves de API

Ninguna fuente usada exige clave. **BCRPData es una API pública de acceso
libre.** El docente puede ejecutar `01_extraccion_api.py` sin configurar nada.
Se entrega `.env.example` por si se incorpora una fuente con token.

## 9. Repositorio

| Campo | Valor |
|---|---|
| URL | https://github.com/SneyderRP/Finanzas-i-tema36-bonos-corporativos |
| Commits | 4 commits en 3 fechas distintas: 22, 23 y 25 de septiembre de 2026 |

## 10. Trazabilidad de tablas y figuras

Todas se regeneran con `04_analisis.py`:

| Salida | Archivo | Sección |
|---|---|---|
| Tabla 1 | `salidas/tabla1_descriptiva.tex` | Materiales y métodos |
| Tabla 2 | `salidas/tabla2_adf.tex` | Materiales y métodos |
| Tabla 3 | `salidas/tabla3_niveles.tex` | Resultados (diagnóstico) |
| Tabla 4 | `salidas/tabla4_variaciones.tex` | Resultados (modelo principal) |
| Figura 1 | `salidas/figura1_series_diarias.png` | Resultados |
| Figura 2 | `salidas/figura2_spread_soberano.png` | Resultados |
| Figura 3 | `salidas/figura3_variaciones.png` | Resultados |
| Figura 4 | `salidas/figura4_riesgo_vs_rendimiento.png` | Resultados |
| Figura 5 | `salidas/figura5_Y_vs_X1.png` | Resultados |
| Figura 6 | `salidas/figura6_Y_vs_X2.png` | Resultados |
| Figura 7 | `salidas/figura7_Y_vs_X3.png` | Resultados |
| Figura 8 | `salidas/figura8_Y_vs_X4.png` | Resultados |
| Figura 9 | `salidas/figura9_matriz_correlaciones.png` | Resultados |
| Tabla 5 | `salidas/tabla5_correlaciones.tex` | Resultados |
| Tabla 6 | `salidas/tabla6_correlaciones_con_Y.tex` | Materiales y métodos |

## 11. Nota metodológica

La regresión en niveles arroja R² de 0,787 pero Durbin-Watson de 0,038, muy
lejos del valor 2 esperado. La prueba de Dickey-Fuller aumentada no rechaza la
hipótesis de raíz unitaria en niveles para cuatro de las cinco series. Se trata
del patrón característico de regresión espuria.

El modelo principal se estima por tanto sobre las **variaciones diarias**, con
R² de 0,139 y Durbin-Watson de 2,087. Ambas estimaciones se reportan: la primera
como diagnóstico, la segunda como resultado.

Los errores estándar son robustos a heterocedasticidad y autocorrelación
(Newey-West, 5 rezagos).

## 12. Versión anterior

La carpeta `version_mensual_descartada/` conserva el primer diseño, un panel de
7 instrumentos de bonos × 180 meses. Se descartó porque mezclaba flujos
(colocaciones) con stocks (saldos) e incluía el agregado del sector privado
junto con sus componentes. Se mantiene como evidencia del proceso de trabajo.

## 13. Citación en APA 7 (numeral 2.4.8)

Banco Central de Reserva del Perú. (2026). *BCRPData: base de datos
estadísticos* [Conjunto de datos]. Consultado el 2026-09-26.
https://estadisticas.bcrp.gob.pe/estadisticas/series/

## 14. Declaración sobre el uso de IA

Se usó asistencia de IA para redactar y depurar el código de extracción, dentro
de lo permitido por la consigna. El estudiante verificó cada código de serie
contra el catálogo oficial del BCRP, cotejó diez observaciones al azar contra la
fuente en vivo con resultado de coincidencia total, y puede explicar cada bloque
del código durante la disertación.
