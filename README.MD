# Eurofins Report Generator

Aplicación de escritorio desarrollada en Python con PyQt5 y ReportLab para la gestión analítica y generación de informes oficiales de laboratorio clonados de Eurofins Alimentario (documentos de 3 páginas con réplicas microbiológicas $n=5$).

## Características

- **Interfaz PyQt5**: Vista simplificada que agrupa los ensayos por muestra ($n=5$), con buscador y selector de carpeta de destino.
- **ReportLab PDF Engine**: Generador multi-página que reproduce la cabecera, metadatos, tabla de trazabilidad, resultados analíticos, pie anclado con acreditación ENAC/ILAC-MRA y firma electrónica.
- **Empaquetado**: Compatible con PyInstaller para compilación directa en ejecutable `.exe`.

## Instalación

```bash
git clone [https://github.com/TU_USUARIO/reportesEurofinsPython.git](https://github.com/TU_USUARIO/reportesEurofinsPython.git)
cd reportesEurofinsPython
pip install -r requirements.txt
```

## Ejecución

```bash
python app.py
```

## Compilación a ejecutable (.exe)

```bash
python -m PyInstaller --noconsole --onefile --collect-all reportlab --hidden-import=PyQt5 --hidden-import=openpyxl --add-data "assets;assets" app.py
```
