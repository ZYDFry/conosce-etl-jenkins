import pandas as pd
import unicodedata
import os

# --- CONFIGURACIÓN DINÁMICA ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(BASE_DIR, "temp_data_raw.pkl")
OUTPUT_FILE = os.path.join(BASE_DIR, "temp_data_transformed.pkl")

# Parámetro Financiero (Tipo de Cambio Referencial)
TIPO_CAMBIO_USD = 3.75

# RAÍCES CLAVE (Tecnología)
# Detecta: Software, Sistemas, Desarrollo, Consultoría, Capacitación...
PALABRAS_CLAVE = [
    #Desarrollo y Sistemas
    'SOFTW', 'SISTEM', 'PLATAFORM', 'DESARROLL', 
    'TECNOLOG', 'DIGITAL', 'APLICACION','WEB','APP',
    #Infraestructura y Redes
    'HARDWARE','INFRAESTRUCTUR','REDES','SERVIDOR','COMPUTO','CLOUD','NUBE',
    'HOSTING','DATACENTER',
    #Datos e IA
    'BIG DATA','DATA', 'ANALYTIC', 'INTELIGENCIA ARTIFICIAL',
    'MACHINE LEARNING', 'AUTOMATIZACION',
    #ERP, CRM y otros sistemas empresariales
    'ERP', 'CRM','SAP','ORACLE','MICROSOFT DYNAMICS','LICENCIA'
    #Seguridad Informática
    'ANTIVIRUS','FIREWALL','ENCRIPTACION','CIBERSEGURIDAD','HACKING'
]
#lista negra para evitar falsos positivos
PALABRAS_EXCLUIR = [
    # Obras y Mantenimiento Físico
    'OBRA', 'CONSTRUCCION', 'MANTENIMIENTO DE VEHICULO', 'PINTURA', 
    'GASFITERIA', 'ALBAÑIL', 'LIMPIEZA', 'JARDINERIA', 'VIGILANCIA',
    #Inmobiliario
    'ARRENDAMIENTO', 'ALQUILER', 'INMUEBLE', 'LOCAL', 'OFICINA', 'EDIFICIO', 'PREDIO',
    # Administrativo y Legal
    'ABOGADO', 'JURIDICO', 'NOTARIA', 'CONTABLE', 'AUDITORIA FINANCIERA',
    'SECRETARIA', 'ASISTENTE ADMINISTRATIVO', 'CHOFER',
    # Defensa y Policial
    'DEFENSA NACIONAL', 'PNP', 'FUERZAS ARMADAS', 'EJERCITO', 'POLICIAL', 
    'MILITAR', 'ARMAMENTO'
    # Palabras trampa de "Desarrollo" no tecnológico
    'DESARROLLO SOCIAL', 'DESARROLLO URBANO', 'DESARROLLO RURAL', 
    'DESARROLLO INFANTIL', 'DESARROLLO ECONOMICO', 'DESARROLLO HUMANO',
    
    # Otros rubros no tecnológicos
    'PUBLICIDAD', 'MARKETING', 'TURISMO', 'CATERING', 'ALIMENTOS', 
    'COCINA', 'COSTURA', 'DEPORTIVO', 'MUSICA', 'TEATRO', 'DANZA',
    'INSUMO', 'MEDICO', 'ENFERMERIA', 'FARMACIA'
]

def corregir_texto(texto):
    """limpiar tildes rotas y caracteres especiales en un texto"""
    if not isinstance(texto,str):
        return str(texto)
    texto = texto.upper()
    texto = texto.replace('CI¿N', 'CIÓN').replace('SI¿N', 'SIÓN')
    texto = texto.replace('ELECTR¿NICO', 'ELECTRÓNICO').replace('INFORM¿TICA', 'INFORMÁTICA')
    texto = texto.replace('TECNOLOG¿A', 'TECNOLOGÍA').replace('EDUCACI¿N', 'EDUCACIÓN')
    texto = texto.replace('ER¿A','ERÍA').replace('TR¿A','TRÍA')
    texto = texto.replace('LOG¿A', 'LOGIA')
    texto = texto.replace('¿', '')
    texto_norm = unicodedata.normalize('NFD',texto)
    texto_st = ''.join(c for c in texto_norm if unicodedata.category(c) != 'Mn')
    return texto_st.strip()

def estadarizar_moneda(df):
    """Normalizar Soles y Dolares"""
    if 'moneda' not in df.columns:
        return df
    df['moneda_limpia'] = df['moneda'].apply(corregir_texto)
    
    #Inicializar con valor por defecto
    df['moneda_normalizada'] = 'DESCONOCIDO'
    # Soles
    mask_soles = df['moneda_limpia'].str.contains('SOL', na=False) | \
                df['moneda_limpia'].str.contains('S/', na=False)
    df.loc[mask_soles, 'moneda_normalizada'] = 'SOLES'

    # Dólares
    mask_dolar = df['moneda_limpia'].str.contains('DOLAR', na=False) | \
                 df['moneda_limpia'].str.contains('USD', na=False) | \
                 df['moneda_limpia'].str.contains('AMERICANO',na = False)
    df.loc[mask_dolar, 'moneda_normalizada'] = 'DOLARES'

    return df

def filtrar_negocio(df):
    print(" -> Aplicando filtros de Consultoría Tech/Edu...")
    
    # 1. Normalizar columnas
    df.columns = df.columns.str.lower().str.strip()
    #2Eliminar duplicados
    total_inicial = len(df)
    df = df.drop_duplicates().copy()
    duplicados_eliminados = total_inicial - len(df)
    # Eliminar columnas vacías
    df = df.dropna(axis=1, how='all')
    if duplicados_eliminados > 0:
        print(f"    - Duplicados eliminados: {duplicados_eliminados}")
    # 3. Eliminar sin monto (si aplica)
    if 'montoreferencial' in df.columns:
        df = df.dropna(subset=['montoreferencial'])
    
    # 4. Filtro Base: Solo SERVICIOS
    if 'objetocontractual' in df.columns:
        df = df[df['objetocontractual'].str.upper() == 'SERVICIO'].copy()
    
      #Conversion Monetaria
    df = estadarizar_moneda(df)
    if 'monto_referencial_item' in df.columns:
        df['monto_total_soles'] = 0.0
        df['tc_utilizado'] = 1.0
        mask_soles = df['moneda_normalizada'] == 'SOLES'
        df.loc[mask_soles, 'monto_total_soles'] = df.loc[mask_soles, 'monto_referencial_item']
        
        mask_dolar = df['moneda_normalizada'] == 'DOLARES'
        df.loc[mask_dolar, 'monto_total_soles'] = df.loc[mask_dolar, 'monto_referencial_item'] * TIPO_CAMBIO_USD
        df.loc[mask_dolar, 'tc_utilizado'] = TIPO_CAMBIO_USD

    # 5. Búsqueda Inteligente (Raíces en Descripción)
    filtro_final= pd.Series([False] * len(df), index=df.index)
    cols_busqueda = ['descripcion_item', 'descripcion_proceso']
    
    for col in cols_busqueda:
        if col in df.columns:
            #Columna temporal limpia
            df[col]= df[col].apply(corregir_texto)
            texto = df[col]
            # Inclusión (Tus palabras nuevas)
            mascara_in = pd.Series([False] * len(df), index=df.index)
            for p in PALABRAS_CLAVE:
                mascara_in |= texto.str.contains(p, regex=False)
                
            # Exclusión (Lista negra reforzada)
            mascara_out = pd.Series([False] * len(df), index=df.index)
            for p in PALABRAS_EXCLUIR:
                mascara_out |= texto.str.contains(p, regex=False)
            
            filtro_final |= (mascara_in & (~mascara_out))

    df_final= df[filtro_final].copy()
    df_final['TIPO_OPORTUNIDAD'] = 'TECH_ADVANCED'

    #Eliminar columnas temporales
    cols_a_borrar = [c for c in df_final.columns if 'moneda_limpia' in c or 'moneda_normalizada' in c]
    df_final = df_final.drop(columns=cols_a_borrar)
    return df_final

def main():
    print("--- 2. TRANSFORMACIÓN ---")
    try:
        if not os.path.exists(INPUT_FILE):
            print("Error: No se encuentra el archivo .pkl (Ejecuta data_read.py)")
            return
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