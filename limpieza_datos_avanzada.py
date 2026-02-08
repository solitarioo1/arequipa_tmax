import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("LIMPIEZA AVANZADA DE DATOS - ESTACIÓN LOMAS")
print("=" * 70)

# Cargar archivo original
df = pd.read_excel('ESTACION_LOMAS.xlsx')

print(f"\nDatos originales: {df.shape[0]} filas")
print(f"\nPrimeros valores únicos en cada columna numérica:")
for col in ['TEMPERATURA MAXIMA (°C)', 'TEMPERATURA MINIMA (°C)', 'HUMEDAD RELATIVA (%)', 'PRECIPITACIÓN (mm/día)']:
    print(f"\n{col}:")
    print(df[col].value_counts().head(10))

# LIMPIEZA PROFUNDA
df_limpio = df.copy()

# 1. Eliminar duplicados
df_limpio = df_limpio.drop_duplicates()
print(f"\n✓ Duplicados eliminados")

# 2. Renombrar columnas para facilitar el trabajo
df_limpio.columns = ['fecha', 'tmax', 'tmin', 'humedad', 'precipitacion']

# 3. Función para limpiar columnas numéricas
def limpiar_numerica(valor):
    """Convierte valores a número, maneja S/D y T"""
    if pd.isna(valor):
        return np.nan
    
    valor = str(valor).strip().upper()
    
    # Casos especiales
    if valor in ['S/D', 'SIN DATOS', '-', '']:
        return np.nan
    if valor == 'T':  # Traza de precipitación = 0.1 mm
        return 0.1
    
    try:
        return float(valor)
    except:
        return np.nan

# 4. Convertir columnas numéricas
print("\n✓ Convirtiendo columnas numéricas...")
for col in ['tmax', 'tmin', 'humedad', 'precipitacion']:
    df_limpio[col] = df_limpio[col].apply(limpiar_numerica)
    print(f"  - {col}: convertida a float64")

# 5. Eliminar filas completamente vacías
filas_antes = len(df_limpio)
df_limpio = df_limpio.dropna(subset=['fecha'])
print(f"\n✓ Filas sin fecha eliminadas: {filas_antes - len(df_limpio)}")

# 6. Manejo de valores nulos en columnas numéricas
print(f"\n✓ Rellenando valores nulos...")
for col in ['tmax', 'tmin', 'humedad', 'precipitacion']:
    nulos = df_limpio[col].isnull().sum()
    if nulos > 0:
        # Para precipitación, rellenar con 0
        if col == 'precipitacion':
            valor_relleno = 0
        else:
            # Para temperaturas y humedad, usar interpolación
            df_limpio[col] = df_limpio[col].interpolate(method='linear')
            # Rellenar los NaN restantes con la media
            valor_relleno = df_limpio[col].mean()
        
        df_limpio[col].fillna(valor_relleno, inplace=True)
        print(f"  - {col}: {nulos} valores nulos reemplazados")

# 7. Eliminar outliers evidentes (valores fuera de rangos lógicos)
print(f"\n✓ Eliminando outliers...")

# Temperaturas: entre -20°C y 50°C
df_limpio = df_limpio[df_limpio['tmax'].between(-20, 50)]
df_limpio = df_limpio[df_limpio['tmin'].between(-20, 50)]
print(f"  - Temperaturas fuera de rango (-20 a 50°C)")

# Humedad: entre 0% y 100%
df_limpio = df_limpio[df_limpio['humedad'].between(0, 100, inclusive='both')]
print(f"  - Humedad fuera de rango (0-100%)")

# Precipitación: no negativa
df_limpio = df_limpio[df_limpio['precipitacion'] >= 0]
print(f"  - Precipitación negativa")

# 8. Ordenar por fecha
df_limpio = df_limpio.sort_values('fecha').reset_index(drop=True)
print(f"\n✓ Datos ordenados por fecha")

# RESUMEN FINAL
print("\n" + "=" * 70)
print("RESUMEN DE LIMPIEZA AVANZADA")
print("=" * 70)

print(f"\nAntes: {df.shape[0]} filas")
print(f"Después: {df_limpio.shape[0]} filas")
print(f"Filas eliminadas: {df.shape[0] - df_limpio.shape[0]} ({(df.shape[0] - df_limpio.shape[0])/df.shape[0]*100:.1f}%)")

print(f"\nValores nulos después de limpieza:")
print(df_limpio.isnull().sum())

print(f"\nESTADÍSTICAS DE DATOS LIMPIOS:")
print(df_limpio.describe())

# EXPORTAR VERSIÓN LIMPIA
df_limpio.to_excel('ESTACION_LOMAS_LIMPIO.xlsx', index=False)
df_limpio.to_csv('ESTACION_LOMAS_LIMPIO.csv', index=False)

print("\n✓ Archivos guardados:")
print("  - ESTACION_LOMAS_LIMPIO.xlsx")
print("  - ESTACION_LOMAS_LIMPIO.csv")

print("\n✓ ¡Limpieza avanzada completada exitosamente!")
print("=" * 70)
