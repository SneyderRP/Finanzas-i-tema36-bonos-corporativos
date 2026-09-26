# Versión mensual descartada

Primer diseño del trabajo: panel de 7 instrumentos de bonos × 180 meses
(1 260 observaciones), con el volumen colocado como variable dependiente.

**No es la base del artículo.**

## Por qué se descartó

- Mezclaba flujos con stocks. La colocación mensual (del orden de 243 millones)
  y el saldo vigente (del orden de 9 226 millones) no son magnitudes
  comparables y no pueden apilarse en la misma variable dependiente.
- Incurría en doble conteo. El agregado «sector privado total» es la suma de
  corporativos, arrendamiento financiero y titulización, y los cuatro convivían
  en el mismo panel.

## Contenido de esta carpeta

- Los cuatro scripts del diseño mensual
- `crudos_mensuales/`: las 13 series mensuales descargadas (códigos PN y PD)
- `salidas_mensuales/`: tablas y figuras de ese diseño
- El panel procesado de 1 260 observaciones

## Diseño vigente

Serie de tiempo diaria 2011-2025 con 3 692 observaciones y cinco variables
sustantivas, en `datos_procesados/datos_procesados_2024200522B.csv`.
Se conserva esta carpeta como evidencia del proceso de trabajo (numeral 2.4.4).
