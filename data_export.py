import pandas as pd
import os

# --- CONFIGURACIÓN DINÁMICA ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(BASE_DIR, "temp_data_transformed.pkl")

# Guardará el Excel en la carpeta "Resultados"
RUTA_SALIDA = os.path.join(BASE_DIR, "Resultados", "Reporte_Oportunidades_OSCE.xlsx")

def main():
    print("--- 3. EXPORTACIÓN A EXCEL ---")
    try:
        df = pd.read_pickle(INPUT_FILE)
        
        # Crear carpeta 'Resultados' si no existe
        os.makedirs(os.path.dirname(RUTA_SALIDA), exist_ok=True)
        
        print(" -> Generando archivo .xlsx...")
        # engine='openpyxl' es obligatorio para escribir Excel modernos
        df.to_excel(RUTA_SALIDA, index=False, engine='openpyxl')
        
        print(f"REPORTE EXCEL GENERADO EN:\n{RUTA_SALIDA}")
        
    except FileNotFoundError:
        print("No hay datos transformados para exportar.")
    except Exception as e:
        print(f"Error al exportar: {e}")

if __name__ == "__main__":
    main()