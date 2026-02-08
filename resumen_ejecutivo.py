import pandas as pd
import warnings
warnings.filterwarnings('ignore')

print("\n" + "=" * 80)
print(" " * 15 + "RESUMEN EJECUTIVO - ANÁLISIS ESTACIÓN LOMAS")
print("=" * 80)

# Cargar datos original y limpio
df_original = pd.read_excel('ESTACION_LOMAS.xlsx')
df_limpio = pd.read_csv('ESTACION_LOMAS_LIMPIO.csv')
df_limpio['fecha'] = pd.to_datetime(df_limpio['fecha'])

print("\n📊 ESTADÍSTICAS DE LA LIMPIEZA DE DATOS")
print("-" * 80)
print(f"Registros originales:        {len(df_original):,}")
print(f"Registros después de limpiar: {len(df_limpio):,}")
print(f"Registros eliminados:         {len(df_original) - len(df_limpio):,} ({(len(df_original) - len(df_limpio))/len(df_original)*100:.1f}%)")
print(f"Periodo de datos:             {df_limpio['fecha'].min().strftime('%d-%m-%Y')} a {df_limpio['fecha'].max().strftime('%d-%m-%Y')}")

print("\n📈 ESTADÍSTICAS POR VARIABLE")
print("-" * 80)

stats = {
    'Temperatura Máxima (°C)': ('tmax', '°C'),
    'Temperatura Mínima (°C)': ('tmin', '°C'),
    'Humedad Relativa (%)': ('humedad', '%'),
    'Precipitación (mm)': ('precipitacion', 'mm')
}

for nombre, (col, unidad) in stats.items():
    media = df_limpio[col].mean()
    minimo = df_limpio[col].min()
    maximo = df_limpio[col].max()
    std = df_limpio[col].std()
    
    print(f"\n{nombre}:")
    print(f"  • Mínimo:       {minimo:.2f} {unidad}")
    print(f"  • Máximo:       {maximo:.2f} {unidad}")
    print(f"  • Promedio:     {media:.2f} {unidad}")
    print(f"  • Desv. Est.:   {std:.2f} {unidad}")

print("\n📅 ANÁLISIS ANUAL")
print("-" * 80)

df_limpio['año'] = df_limpio['fecha'].dt.year
resumen_anual = df_limpio.groupby('año').agg({
    'tmax': ['min', 'max', 'mean'],
    'tmin': ['min', 'max', 'mean'],
    'humedad': 'mean',
    'precipitacion': 'sum'
}).round(2)

for año in df_limpio['año'].unique():
    datos_año = df_limpio[df_limpio['año'] == año]
    print(f"\nAÑO {año}:")
    print(f"  • Registros:        {len(datos_año)}")
    print(f"  • Tmax (°C):        Mín: {datos_año['tmax'].min():.1f}°C | Prom: {datos_año['tmax'].mean():.1f}°C | Máx: {datos_año['tmax'].max():.1f}°C")
    print(f"  • Tmin (°C):        Mín: {datos_año['tmin'].min():.1f}°C | Prom: {datos_año['tmin'].mean():.1f}°C | Máx: {datos_año['tmin'].max():.1f}°C")
    print(f"  • Humedad (%):      {datos_año['humedad'].mean():.1f}%")
    print(f"  • Precipitación:    {datos_año['precipitacion'].sum():.1f} mm")

print("\n📂 ARCHIVOS GENERADOS")
print("-" * 80)
archivos = [
    ("ESTACION_LOMAS_LIMPIO.xlsx", "Datos limpios en formato Excel"),
    ("ESTACION_LOMAS_LIMPIO.csv", "Datos limpios en formato CSV"),
    ("GRAFICOS_COMPARATIVOS_POR_AÑO.png", "Gráficos de comparación mensual por año"),
    ("RESUMEN_ANUAL.csv", "Resumen estadístico anual"),
    ("limpieza_datos_avanzada.py", "Script de limpieza de datos"),
    ("generar_graficos.py", "Script para generar gráficos"),
]

for archivo, descripcion in archivos:
    print(f"  ✓ {archivo:.<50} {descripcion}")

print("\n🔍 PROBLEMAS IDENTIFICADOS Y CORREGIDOS")
print("-" * 80)
problemas = [
    ("Valores faltantes", "126 temperaturas máximas, 123 mínimas, 142 humedad, 111 precipitación"),
    ("Valores especiales", "Marcas 'S/D' (sin dato) y 'T' (traza de precipitación)"),
    ("Tipo de datos", "Columnas numéricas estaban almacenadas como texto"),
    ("Outliers", "Una inversión de temperatura y valores negativos de precipitación"),
    ("Duplicados", "1 registro duplicado el 2024-02-01"),
]

for i, (problema, solucion) in enumerate(problemas, 1):
    print(f"  {i}. {problema}")
    print(f"     → {solucion}")

print("\n✅ LIMPIEZA COMPLETADA EXITOSAMENTE")
print("=" * 80)
print("\nLos datos están listos para análisis, reportes y gráficos de comparación.\n")
ñ