# Meglinho Sneyder Rojas Poma
# Codigo de matricula: 2024200522B
# Tema 36 del temario: Bonos corporativos en el mercado peruano: colocaciones, tasas y plazos
# Fecha de extraccion: 2026-09-22

"""Parametros compartidos. La consulta se CONGELA aqui (numeral 2.4.5)."""
from pathlib import Path

CODIGO_MATRICULA = "2024200522B"
SEMILLA = 522                      # cuatro ultimos digitos del codigo

FECHA_INICIO, FECHA_CORTE = "2011-01-01", "2025-12-31"
BCRP_INICIO, BCRP_FIN = "2011-1", "2025-12"

RAIZ = Path(__file__).resolve().parent.parent
DIR_CRUDOS = RAIZ / "datos_crudos"
DIR_POR_VARIABLE = DIR_CRUDOS / "por_variable"
DIR_PROCESADOS = RAIZ / "datos_procesados"
DIR_SALIDAS = RAIZ / "salidas"
LOG = RAIZ / "log_ejecucion.txt"

for c in (DIR_CRUDOS, DIR_POR_VARIABLE, DIR_PROCESADOS, DIR_SALIDAS):
    c.mkdir(parents=True, exist_ok=True)

ARCHIVO_CRUDO = DIR_CRUDOS / f"datos_crudos_api_{CODIGO_MATRICULA}.csv"
ARCHIVO_PROCESADO = DIR_PROCESADOS / f"datos_procesados_{CODIGO_MATRICULA}.csv"

USER_AGENT = ("UNCP-FacultadEconomia-FinanzasI/1.0 (trabajo academico; "
              "contacto: e_2024200522B@uncp.edu.pe)")
PAUSA, TIMEOUT = 1.5, 30
