# Base de datos y código — Unidad I

**Estudiante:** ROJAS POMA, MEGLINHO SNEYDER
**Código de matrícula:** 2024200522B
**Curso:** Finanzas I (055D) · Escuela Profesional de Economía · UNCP · 2026-II
**Tema del temario:** N.º 36 — Bonos corporativos en el mercado peruano: colocaciones, tasas y plazos
**Docente:** Dr. Ciro Iván Machacuay Meza

## 1. Objetivo

Analizar los determinantes del monto colocado de bonos en el mercado peruano
según el costo de oportunidad del financiamiento y el riesgo país, distinguiendo
por tipo de instrumento y por tramo de plazo.

**Diseño:** panel de 7 instrumentos × 180 meses = 1260 observaciones.
**Llave:** `instrumento` + `fecha`.
**Dependiente:** `log_monto` = ln(1 + monto en millones de S/).
**Explicativas:** tasa de referencia, prima por plazo, riesgo país (EMBIG) y
spread bancario corporativo, con efectos fijos por instrumento.

## 2. Fuente y endpoint

| Campo | Valor |
|---|---|
| Fuente | BCRPData, Banco Central de Reserva del Perú |
| Tipo | API REST pública, sin clave de acceso |
| Endpoint | `https://estadisticas.bcrp.gob.pe/estadisticas/series/api/{código}/json/{inicio}/{fin}/esp` |
| Series | 13, todas mensuales. Ver `diccionario_variables.md` |
| Fecha de consulta | 2026-09-22 |

Cada serie se descarga por separado y se guarda en `datos_crudos/por_variable/`,
para poder cotejarla una por una con la fuente oficial (numeral 2.4.6).

**Vía 2.** El numeral 2.4.1 exige una sola vía automatizada en la Unidad I,
preferentemente API, y la vía API cubre el 100 % de las variables. Se entrega
`02_scraping_web.py` como verificación cruzada opcional.

## 3. Ventana congelada (numeral 2.4.5)

| Parámetro | Valor |
|---|---|
| `FECHA_INICIO` | 2011-01-01 |
| `FECHA_CORTE` | 2025-12-31 |

Declarados como constantes en `codigo/00_config.py`. Ningún script usa la fecha
del día, para que la consulta sea reproducible.

## 4. Orden de ejecución

```bash
cd codigo
pip install -r ../requirements.txt

python 01_extraccion_api.py    # vía API      -> /datos_crudos
python 02_scraping_web.py      # verificación -> /datos_crudos
python 03_limpieza_datos.py    # panel        -> /datos_procesados
python 04_analisis.py          # tablas y figuras -> /salidas
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
| SHA-256 | `92574a78aa72ad9c0cf5ee679fb2b455b3c46823c5341140d11bf42cc3a83dbd` |
| Filas | 1260 |
| Columnas | 19 |

El hash se coteja contra el archivo entregado, nunca contra una reejecución
posterior (numeral 2.4.5).

## 7. Claves de API

Ninguna fuente usada exige clave. Se entrega `.env.example` con los nombres de
variables por si se incorpora una fuente con token.

## 8. Repositorio

| Campo | Valor |
|---|---|
| URL | https://github.com/SneyderRP/Finanzas-i-tema36-bonos-corporativos |
| Commits | 1 de 3. Historial en la pestaña Commits del repositorio |

## 9. Trazabilidad de tablas y figuras

Todas se regeneran con `04_analisis.py`:

| Salida | Archivo | Sección del artículo |
|---|---|---|
| Tabla 1 | `salidas/tabla1_descriptiva.tex` | Materiales y métodos |
| Tabla 2 | `salidas/tabla2_por_instrumento.tex` | Materiales y métodos |
| Tabla 3 | `salidas/tabla3_panel_efectos_fijos.tex` | Resultados |
| Tabla 4 | `salidas/tabla4_robustez_corporativos.tex` | Resultados |
| Figura 1 | `salidas/figura1_colocacion_anual.png` | Resultados |
| Figura 2 | `salidas/figura2_tasas_y_riesgo.png` | Resultados |
| Figura 3 | `salidas/figura3_tasa_vs_colocacion.png` | Resultados |
| Figura 4 | `salidas/figura4_saldos_por_plazo.png` | Resultados |

## 10. Citación en APA 7 (numeral 2.4.8)

Banco Central de Reserva del Perú. (2026). *BCRPData: base de datos estadísticos*
[Conjunto de datos]. Consultado el 2026-09-22.
https://estadisticas.bcrp.gob.pe/estadisticas/series/

## 11. Declaración sobre el uso de IA

Se usó asistencia de IA para redactar y depurar el código de extracción, dentro
de lo permitido por la consigna. El estudiante verificó cada código de serie
contra el catálogo oficial del BCRP, cotejó los datos con la fuente y puede
explicar cada bloque del código durante la disertación.
