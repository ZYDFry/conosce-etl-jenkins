#  Motor de Búsqueda de Oportunidades Tecnológicas (OSCE)

Este proyecto es un **Pipeline ETL (Extract, Transform, Load)** automatizado en Python diseñado para analizar miles de licitaciones del estado y detectar oportunidades de negocio específicas para el sector de **Tecnología y Software**, eliminando el ruido de otros rubros.

## Características Principales (Versión 1.6)

El algoritmo cuenta con una lógica de filtrado avanzada ("Blindada") que resuelve problemas comunes de calidad de datos:

### 1. Limpieza de Texto Híbrida (Unicode + Patrones)
- **Problema:** La data original contenía caracteres corruptos (`TECNOLOG¿A`, `GESTI¿N`) y tildes ocultas.
- **Solución:** Implementación de normalización `Unicode (NFD)` y reparación de patrones. El reporte final entrega textos limpios y estandarizados (ej: `MAESTRIA EN DIRECCION`).

### 2. Detección Inteligente de Moneda
- **Problema:** El sistema no reconocía "Dólar Norteamericano" por la tilde, asignando valor 0.
- **Solución:** Algoritmo insensible a tildes (`Dólar` = `DOLAR`) que aplica automáticamente el Tipo de Cambio (S/ 3.75) para unificar todo a Soles.

### 3. Filtro Semántico de "Listas Negras"
- **Inclusión:** Busca raíces clave (`SOFTW`, `CLOUD`, `BIG DATA`, `IA`).
- **Exclusión:** Elimina falsos positivos mediante un filtro de contexto negativo.
  - *Ejemplo:* Bloquea "Maestrías en **Defensa** Nacional" aunque contengan la palabra "Desarrollo".
  - *Ejemplo:* Bloquea "Alquiler de **Inmuebles**" para sistemas.

---

##  Tecnologías Usadas
* **Python 3.x**
* **Pandas:** Manipulación eficiente de DataFrames.
* **Unicodedata:** Tratamiento profesional de codificación de texto.
* **Git/GitHub:** Control de versiones con flujo de ramas (`develop` -> `main`).

---

##  Instalación y Uso

1. **Clonar el repositorio:**
   ```bash
   git clone <URL_DE_TU_REPO>
