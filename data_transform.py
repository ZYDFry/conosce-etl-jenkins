import pandas as pd
import os

# --- CONFIGURACIÓN DINÁMICA ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(BASE_DIR, "temp_data_raw.pkl")
OUTPUT_FILE = os.path.join(BASE_DIR, "temp_data_transformed.pkl")

# RAÍCES CLAVE (Tecnología + Educación)
# Detecta: Software, Sistemas, Desarrollo, Consultoría, Maestría, Capacitación...
PALABRAS_CLAVE = [
    'SOFTW', 'SISTEM', 'PLATAFORM', 'DESARROLL', 
    'TECNOLOG', 'DIGITAL', 'CONSULTOR', 'MAESTR', 
    'CAPACITA', 'TALLER', 'CURSO', 'LICENCIA', 'SERVIDOR'
]

def filtrar_negocio(df):
    print(" -> Aplicando filtros de Consultoría Tech/Edu...")
    
    # 1. Normalizar columnas
    df.columns = df.columns.str.lower().str.strip()
    #2Eliminar duplicados
    total_inicial = len(df)
    df = df.drop_duplicates().copy()
    duplicados_eliminados = total_inicial - len(df)
    if duplicados_eliminados > 0:
        print(f"    - Duplicados eliminados: {duplicados_eliminados}")
    # 3. Eliminar sin monto (si aplica)
    if 'montoreferencial' in df.columns:
        df = df.dropna(subset=['montoreferencial'])
        
    # 4. Filtro Base: Solo SERVICIOS
    if 'objetocontractual' in df.columns:
        df = df[df['objetocontractual'].str.upper() == 'SERVICIO'].copy()
    
    # 5. Búsqueda Inteligente (Raíces en Descripción)
    filtro_tech = pd.Series([False] * len(df), index=df.index)
    cols_busqueda = ['descripcion_item', 'descripcion_proceso']
    
    for col in cols_busqueda:
        if col in df.columns:
            # Convertimos a mayúsculas temporalmente para buscar
            texto_col = df[col].astype(str).str.upper()
            for raiz in PALABRAS_CLAVE:
                filtro_tech |= texto_col.str.contains(raiz, regex=False)

    df_final = df[filtro_tech].copy()
    df_final['TIPO_OPORTUNIDAD'] = 'TECH_EDUCACION'
    
    return df_final

def main():
    print("--- 2. TRANSFORMACIÓN ---")
    try:
        df = pd.read_pickle(INPUT_FILE)
        
        df_transformado = filtrar_negocio(df)
        
        df_transformado.to_pickle(OUTPUT_FILE)
        print(f"TRANSFORMACIÓN EXITOSA.")
        print(f"Entrada: {len(df)} -> Oportunidades detectadas: {len(df_transformado)}")
        
    except FileNotFoundError:
        print("Error: Ejecuta data_read.py primero.")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()