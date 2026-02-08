import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("GENERANDO GRÁFICOS COMPARATIVOS POR AÑO")
print("=" * 70)

# Cargar datos limpios
df = pd.read_csv('ESTACION_LOMAS_LIMPIO.csv')
df['fecha'] = pd.to_datetime(df['fecha'])

# Extraer año y mes
df['año'] = df['fecha'].dt.year
df['mes'] = df['fecha'].dt.month
df['mes_nombre'] = df['fecha'].dt.strftime('%b')

# Agrupar por año y mes
datos_mensuales = df.groupby(['año', 'mes']).agg({
    'tmax': 'mean',
    'tmin': 'mean',
    'humedad': 'mean',
    'precipitacion': 'sum'
}).reset_index()

# Obtener años disponibles
años = sorted(df['año'].unique())
print(f"\nAños en los datos: {años}")

# Crear figura con 4 subplots
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('ESTACIÓN LOMAS - COMPARATIVA MENSUAL POR AÑO', fontsize=16, fontweight='bold')

# Colores para cada año
colores = {
    2018: '#1f77b4',  # Azul
    2019: '#ff7f0e',  # Naranja
    2020: '#2ca02c',  # Verde
    2021: '#d62728',  # Rojo
    2022: '#9467bd',  # Púrpura
    2023: '#8c564b',  # Marrón
    2024: '#e377c2',  # Rosa
    2025: '#7f7f7f',  # Gris
    2026: '#bcbd22'   # Amarillo verdoso
}

# 1. TEMPERATURA MÁXIMA
ax1 = axes[0, 0]
for año in años:
    datos_año = datos_mensuales[datos_mensuales['año'] == año]
    ax1.plot(datos_año['mes'], datos_año['tmax'], 
             marker='o', linewidth=2, label=str(año), color=colores.get(año, None))

ax1.set_xlabel('Mes', fontweight='bold')
ax1.set_ylabel('Temperatura (°C)', fontweight='bold')
ax1.set_title('TEMPERATURA MÁXIMA PROMEDIO MENSUAL', fontweight='bold')
ax1.set_xticks(range(1, 13))
ax1.set_xticklabels(['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'])
ax1.legend(loc='best', fontsize=9)
ax1.grid(True, alpha=0.3)

# 2. TEMPERATURA MÍNIMA
ax2 = axes[0, 1]
for año in años:
    datos_año = datos_mensuales[datos_mensuales['año'] == año]
    ax2.plot(datos_año['mes'], datos_año['tmin'], 
             marker='s', linewidth=2, label=str(año), color=colores.get(año, None))

ax2.set_xlabel('Mes', fontweight='bold')
ax2.set_ylabel('Temperatura (°C)', fontweight='bold')
ax2.set_title('TEMPERATURA MÍNIMA PROMEDIO MENSUAL', fontweight='bold')
ax2.set_xticks(range(1, 13))
ax2.set_xticklabels(['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'])
ax2.legend(loc='best', fontsize=9)
ax2.grid(True, alpha=0.3)

# 3. HUMEDAD RELATIVA
ax3 = axes[1, 0]
for año in años:
    datos_año = datos_mensuales[datos_mensuales['año'] == año]
    ax3.plot(datos_año['mes'], datos_año['humedad'], 
             marker='^', linewidth=2, label=str(año), color=colores.get(año, None))

ax3.set_xlabel('Mes', fontweight='bold')
ax3.set_ylabel('Humedad Relativa (%)', fontweight='bold')
ax3.set_title('HUMEDAD RELATIVA PROMEDIO MENSUAL', fontweight='bold')
ax3.set_xticks(range(1, 13))
ax3.set_xticklabels(['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'])
ax3.set_ylim([70, 100])
ax3.legend(loc='best', fontsize=9)
ax3.grid(True, alpha=0.3)

# 4. PRECIPITACIÓN
ax4 = axes[1, 1]
for año in años:
    datos_año = datos_mensuales[datos_mensuales['año'] == año]
    ax4.bar(datos_año['mes'] + (años.index(año) - len(años)/2) * 0.1, 
            datos_año['precipitacion'], 
            width=0.08, label=str(año), color=colores.get(año, None), alpha=0.7)

ax4.set_xlabel('Mes', fontweight='bold')
ax4.set_ylabel('Precipitación (mm)', fontweight='bold')
ax4.set_title('PRECIPITACIÓN ACUMULADA MENSUAL', fontweight='bold')
ax4.set_xticks(range(1, 13))
ax4.set_xticklabels(['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'])
ax4.legend(loc='best', fontsize=9)
ax4.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('GRAFICOS_COMPARATIVOS_POR_AÑO.png', dpi=300, bbox_inches='tight')
print("\n✓ Gráfico guardado: GRAFICOS_COMPARATIVOS_POR_AÑO.png")

plt.show()

# Crear tabla resumen anual
print("\n" + "=" * 70)
print("RESUMEN ANUAL")
print("=" * 70)

resumen_anual = df.groupby('año').agg({
    'tmax': ['min', 'max', 'mean'],
    'tmin': ['min', 'max', 'mean'],
    'humedad': 'mean',
    'precipitacion': 'sum'
}).round(2)

print("\nResumen por año:")
print(resumen_anual)

# Exportar resumen a CSV
resumen_anual.to_csv('RESUMEN_ANUAL.csv')
print("\n✓ Resumen anual guardado en: RESUMEN_ANUAL.csv")

print("\n" + "=" * 70)
print("✓ ¡Gráficos generados exitosamente!")
print("=" * 70)
