import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Cargar archivo
print("=" * 70)
print("CARGANDO DATOS DE LA ESTACIÓN LOMAS")
print("=" * 70)

try:
    df = pd.read_excel('ESTACION_LOMAS.xlsx')
    print(f"✓ Archivo cargado exitosamente")
    print(f"  Dimensiones: {df.shape[0]} filas x {df.shape[1]} columnas")
except Exception as e:
    print(f"✗ Error al cargar: {e}")
    exit()

# EXPLORACIÓN INICIAL
print("\n" + "=" * 70)
print("1. EXPLORACIÓN INICIAL")
print("=" * 70)

print("\nNombres de columnas:")
print(df.columns.tolist())

print("\nPrimeras 5 filas:")
print(df.head())

print("\nTipos de datos:")
print(df.dtypes)

print("\nInfo del DataFrame:")
print(df.info())

# ANÁLISIS DE VALORES NULOS
print("\n" + "=" * 70)
print("2. ANÁLISIS DE VALORES NULOS")
print("=" * 70)

nulos = df.isnull().sum()
print(f"\nValores nulos por columna:")
print(nulos)

porcentaje_nulos = (df.isnull().sum() / len(df) * 100).round(2)
print(f"\nPorcentaje de valores nulos:")
print(porcentaje_nulos)

# DETECCIÓN DE DUPLICADOS
print("\n" + "=" * 70)
print("3. ANÁLISIS DE DUPLICADOS")
print("=" * 70)

duplicados = df.duplicated().sum()
print(f"\nFilas duplicadas: {duplicados}")

if duplicados > 0:
    print(f"Índices de filas duplicadas:")
    print(df[df.duplicated(keep=False)].sort_values(list(df.columns)).head(10))

# ESTADÍSTICAS BÁSICAS
print("\n" + "=" * 70)
print("4. ESTADÍSTICAS BÁSICAS")
print("=" * 70)

print(df.describe())

# LIMPIEZA DE DATOS
print("\n" + "=" * 70)
print("INICIANDO LIMPIEZA DE DATOS")
print("=" * 70)

df_limpio = df.copy()

# 1. Eliminar duplicados
duplicados_antes = len(df_limpio)
df_limpio = df_limpio.drop_duplicates()
print(f"\n✓ Duplicados eliminados: {duplicados_antes - len(df_limpio)}")

# 2. Manejar valores nulos
print(f"\n✓ Manejo de valores nulos:")
for col in df_limpio.columns:
    if df_limpio[col].isnull().any():
        if df_limpio[col].dtype in ['float64', 'int64']:
            # Para columnas numéricas, usar la media
            media = df_limpio[col].mean()
            df_limpio[col].fillna(media, inplace=True)
            print(f"  - {col}: reemplazado con media ({media:.2f})")
        else:
            # Para columnas de texto, usar la moda o 'Sin Datos'
            moda = df_limpio[col].mode()
            if len(moda) > 0:
                df_limpio[col].fillna(moda[0], inplace=True)
                print(f"  - {col}: reemplazado con moda ({moda[0]})")
            else:
                df_limpio[col].fillna('Sin Datos', inplace=True)
                print(f"  - {col}: reemplazado con 'Sin Datos'")

# 3. Convertir columnas de fecha si existen
print(f"\n✓ Conversión de formatos:")
for col in df_limpio.columns:
    if 'fecha' in col.lower() or 'date' in col.lower():
        try:
            df_limpio[col] = pd.to_datetime(df_limpio[col])
            print(f"  - {col}: convertido a datetime")
        except:
            print(f"  - {col}: no se pudo convertir")

# 4. Limpiar espacios en blanco
for col in df_limpio.select_dtypes(include=['object']).columns:
    df_limpio[col] = df_limpio[col].str.strip() if df_limpio[col].dtype == 'object' else df_limpio[col]
    print(f"  - {col}: espacios en blanco eliminados")

# 5. Detección de valores atípicos (outliers)
print(f"\n✓ Detección de valores atípicos:")
outliers_totales = 0
for col in df_limpio.select_dtypes(include=[np.number]).columns:
    Q1 = df_limpio[col].quantile(0.25)
    Q3 = df_limpio[col].quantile(0.75)
    IQR = Q3 - Q1
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR
    
    outliers = df_limpio[(df_limpio[col] < limite_inferior) | (df_limpio[col] > limite_superior)]
    if len(outliers) > 0:
        print(f"  - {col}: {len(outliers)} valores atípicos detectados")
        outliers_totales += len(outliers)

# RESUMEN FINAL
print("\n" + "=" * 70)
print("RESUMEN DE LIMPIEZA")
print("=" * 70)

print(f"\nAntes de la limpieza:  {len(df)} filas x {len(df.columns)} columnas")
print(f"Después de la limpieza: {len(df_limpio)} filas x {len(df_limpio.columns)} columnas")
print(f"Filas eliminadas: {len(df) - len(df_limpio)}")

print(f"\nValores nulos restantes: {df_limpio.isnull().sum().sum()}")
print(f"Duplicados restantes: {df_limpio.duplicated().sum()}")

# EXPORTAR DATOS LIMPIOS
print("\n" + "=" * 70)
print("EXPORTANDO DATOS LIMPIOS")
print("=" * 70)

df_limpio.to_excel('ESTACION_LOMAS_LIMPIO.xlsx', index=False)
print("✓ Archivo limpio guardado: ESTACION_LOMAS_LIMPIO.xlsx")

df_limpio.to_csv('ESTACION_LOMAS_LIMPIO.csv', index=False)
print("✓ Archivo limpio guardado: ESTACION_LOMAS_LIMPIO.csv")

print("\n✓ ¡Limpieza completada exitosamente!")
print("=" * 70)
