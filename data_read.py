import pandas as pd
import glob
import os

# --- CONFIGURACIÓN DINÁMICA ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_DATASETS = os.path.join(BASE_DIR, "datasets")
ARCHIVO_TEMP = os.path.join(BASE_DIR, "temp_data_raw.pkl")

def cargar_datos_osce():
    print(f"--- 1. LECTURA: Buscando Excels en {RUTA_DATASETS} ---")
    
    patron = os.path.join(RUTA_DATASETS, "*.xlsx")
    archivos = glob.glob(patron)
    
    if not archivos:
        print("No se encontraron archivos .xlsx.")
        return None

    lista_dfs = []
    for archivo in archivos:
        nombre = os.path.basename(archivo)
        
        # ---SEGURIDAD ANTI-BUCLE ---
        # Si el archivo es un temporal de Excel (~$) o es nuestro propio REPORTE de salida, lo saltamos.
        if nombre.startswith("~$") or "REPORTE" in nombre.upper() or "RESULTADO" in nombre.upper():
            print(f"Saltando archivo de salida/sistema: {nombre}")
            continue
        # -----------------------------

        print(f" -> Leyendo: {nombre}")
        try:
            df = pd.read_excel(archivo, engine='openpyxl')
            lista_dfs.append(df)
        except Exception as e:
            print(f"Error leyendo {nombre}: {e}")

    if lista_dfs:
        return pd.concat(lista_dfs, ignore_index=True)
    else:
        return None

def main():
    df = cargar_datos_osce()
    if df is not None:
        df.to_pickle(ARCHIVO_TEMP)
        print(f"LECTURA COMPLETA. Total registros crudos: {len(df)}")
    else:
        print("El proceso terminó sin datos.")

if __name__ == "__main__":
    main()