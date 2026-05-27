# Autor: Dagoberto Santisteban
# Descripción: Limpieza, transformación y exportación de datos de comparendos para Power BI
# Fecha: 2026-05-28

import pandas as pd

# ============================================
# 1. CARGA DE DATOS
# ============================================

print(" Cargando archivo CSV...")
ruta = r"C:\Users\PC\Downloads\IMPOSICIÓN_DE_COMPARENDOS_DE_TRANSITO_EN_EL_MUNICIPIO_DE_CHÍA_20260526.csv"

# Cargar CSV usando la primera fila como encabezado
df = pd.read_csv(ruta)

# Renombrar columnas para estandarizar
df.columns = ['VIGENCIA', 'NUMERO_COMPARENDO', 'FECHA_IMPOSICION', 'INFRACCION', 'TIPO_COMPARENDO']

print(f" Registros cargados: {len(df)}")
print(df.head())

# ============================================
# 2. LIMPIEZA DE DATOS
# ============================================

print("\n Iniciando limpieza...")

# Eliminar nulos y duplicados
df = df.dropna()
df = df.drop_duplicates(subset=['NUMERO_COMPARENDO'])

# Limpiar columnas numéricas (quitar comas y puntos)
df['VIGENCIA'] = df['VIGENCIA'].astype(str).str.replace(',', '').str.replace('.', '').astype(int)
df['NUMERO_COMPARENDO'] = df['NUMERO_COMPARENDO'].astype(str).str.replace(',', '').str.replace('.', '')

print(f" Registros después de limpieza: {len(df)}")

# ============================================
# 3. PROCESAMIENTO DE FECHAS
# ============================================

print("\nProcesando fechas...")

# Convertir a datetime
df['FECHA_IMPOSICION'] = pd.to_datetime(
    df['FECHA_IMPOSICION'], 
    format='%Y %b %d %I:%M:%S %p', 
    errors='coerce'
)

# Eliminar fechas inválidas
df = df.dropna(subset=['FECHA_IMPOSICION'])
print(f" Registros con fechas válidas: {len(df)}")

# ============================================
# 4. COLUMNAS DERIVADAS
# ============================================

print("\n➕ Creando columnas para análisis...")

df['AÑO'] = df['FECHA_IMPOSICION'].dt.year
df['MES_NUM'] = df['FECHA_IMPOSICION'].dt.month
df['MES_NOMBRE'] = df['FECHA_IMPOSICION'].dt.month_name()
df['DIA_SEMANA_NUM'] = df['FECHA_IMPOSICION'].dt.dayofweek
df['DIA_SEMANA_NOMBRE'] = df['FECHA_IMPOSICION'].dt.day_name()
df['DIA_MES'] = df['FECHA_IMPOSICION'].dt.day
df['TRIMESTRE'] = df['FECHA_IMPOSICION'].dt.quarter

print(" Columnas derivadas creadas")

# ============================================
# 5. EXPORTAR Y ESTADÍSTICAS
# ============================================

print("\n Exportando archivo limpio...")

# Ordenar y resetear índice
df = df.sort_values('FECHA_IMPOSICION').reset_index(drop=True)

# Exportar a CSV
ruta_salida = r"C:\Users\PC\Downloads\comparendos_chia_limpio.csv"
df.to_csv(ruta_salida, index=False, encoding='utf-8-sig')

print(f" Archivo exportado: {ruta_salida}")

# Mostrar resumen final
print(f"\n{'='*60}")
print(f"RESUMEN FINAL")
print(f"{'='*60}")
print(f"Total de comparendos: {len(df):,}")
print(f"Rango de fechas: {df['FECHA_IMPOSICION'].min().date()} a {df['FECHA_IMPOSICION'].max().date()}")
print(f"\nDistribución por año:")
print(df['AÑO'].value_counts().sort_index())
print(f"\nTop 5 infracciones:")
print(df['INFRACCION'].value_counts().head())
print(f"{'='*60}")

