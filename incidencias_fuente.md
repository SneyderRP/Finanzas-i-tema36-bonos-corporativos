# Incidencias de fuente

Registro de limitaciones tecnicas de las fuentes consultadas (numeral 2.4.3).

## 1. BCRPData — sin incidencias

La via API respondio HTTP 200 en las cinco series diarias consultadas, sin
bloqueos ni restricciones. El detalle de cada solicitud, con fecha, hora y
nombre oficial de la serie devuelta, esta en `log_ejecucion.txt`.

| Variable | Codigo | Serie oficial |
|---|---|---|
| Y | `PD31893DD` | Rendimiento del Bono del gobierno peruano a 10 anos (en S/) |
| X1 | `PD12301MD` | Tasa de Referencia de la Politica Monetaria |
| X2 | `PD04719XD` | Bonos del Tesoro EE.UU. - 10 anos (%) |
| X3 | `PD04709XD` | Spread - EMBIG Peru (pbs) |
| X4 | `PD04692MD` | Interbancaria, S/ |

## 2. SMV — exploracion documentada el 2026-09-23

Se exploro el portal de la Superintendencia del Mercado de Valores buscando la
tasa de colocacion por emision y la clasificacion de riesgo del emisor, dos
variables del temario que no existen como serie en BCRPData.

**Resultado de la exploracion:**

- `https://www.smv.gob.pe/` responde HTTP 200, pero redirige a
  `https://www.gob.pe/smv`, la ficha institucional de la SMV dentro del portal
  unico del Estado, no el sistema de informacion.
- No existe `robots.txt`: la ruta `/robots.txt` devuelve la pagina de inicio
  completa (270 843 caracteres, con `<!DOCTYPE html>`), comportamiento propio
  de una aplicacion de pagina unica.
- El sistema de informacion (SIMV) esta en `https://www.smv.gob.pe/SIMV/`.
- **Cada consulta del SIMV requiere un parametro `data=` de 42 caracteres
  hexadecimales**, por ejemplo:
  `https://www.smv.gob.pe/simv/Frm_Opas?data=B0BAD43B72085E6947D724B1B24FA334D125F9653C`
  Ese token se genera del lado del servidor y cambia por sesion, por lo que no
  puede construirse desde un script ni reutilizarse entre ejecuciones.
- La mesa de partes y el acceso de colaboradores exigen autenticacion
  (`mvnet.smv.gob.pe/mvnet/Autenticacion/frmInicio.aspx`).

**Conclusion.** El SIMV no expone las emisiones en un formato accesible por via
automatizada con las herramientas propias del ciclo V. Corresponde al supuesto
del numeral 2.4.3: contenido dinamico servido por sesion.

**Decision adoptada.** No se solicita sustitucion de fuente, porque no procede:
la Unidad I exige una sola via automatizada (numeral 2.4.1) y la via API de
BCRPData la cumple integramente, cubriendo las cinco variables sustantivas del
modelo.

Las dos variables no disponibles se sustituyen por proxies declarados en
Materiales y metodos:

| Variable del temario | Sustituto | Justificacion |
|---|---|---|
| Tasa de colocacion por emision | `Y_rendimiento_soberano` (`PD31893DD`) | Tasa base del mercado de bonos peruano: ninguna emision corporativa local se coloca por debajo del soberano al mismo plazo |
| Clasificacion de riesgo del emisor | `X3_riesgo_pais` (`PD04709XD`) | Riesgo crediticio puesto en precio por el mercado, en lugar de calificado por una agencia privada |

**Etica del rastreo (numeral 2.4.8).** Todas las solicitudes se realizaron con
User-Agent identificable, con pausas entre peticiones, sobre informacion
publica y sin intentar vulnerar ningun acceso restringido.
