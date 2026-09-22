import os
import sys
import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QStatusBar,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

# Motor de generación oficial de 3 páginas
import pdf_generator


def get_official_filename(row_item):
    """Nomenclatura oficial limpia sin espacios ni caracteres codificados:

    [sample code Nr]-[Client reference]-[Sample reference]-[Analytical Report
    Nr].pdf
    """
    sample_code = str(row_item.get("Sample Code (Eurofins)", "")).strip()
    client_ref = (
        str(row_item.get("Ref. Cliente (Lote/Exp)", "")).strip().replace("/", "_")
    )
    # Limpiamos barras y espacios sobrantes del nombre de la muestra/producto
    sample_ref = (
        str(row_item.get("Producto / Muestra", ""))
        .replace("/", "")
        .strip()
        .replace(" ", "_")
    )
    ar_nr = str(row_item.get("Informe Analítico (AR)", "")).strip().replace("/", "_")
    return f"{sample_code}-{client_ref}-{sample_ref}-{ar_nr}.pdf"


class EurofinsReportApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Eurofins Report Generator - Gestor de Muestras (n=5)")
        self.resize(1240, 720)

        self.df_raw = None
        self.df_samples = None
        self.excel_file_path = ""

        # Carpeta de salida predeterminada (Escritorio/informes_generados)
        desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")
        self.output_directory = os.path.join(desktop_dir, "informes_generados")

        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(10)

        # --- FILA 1: BOTONES DE ACCIÓN Y BUSCADOR ---
        top_bar = QHBoxLayout()
        top_bar.setSpacing(10)

        self.btn_open = QPushButton("📂 Cargar Base de Datos Excel")
        self.btn_open.setFixedHeight(38)
        self.btn_open.setStyleSheet(
            "QPushButton {"
            " background-color: #002B49;"
            " color: #FFFFFF;"
            " font-size: 12px;"
            " font-weight: bold;"
            " border-radius: 4px;"
            " padding: 0 16px;"
            "}"
            "QPushButton:hover { background-color: #001A2C; }"
        )
        self.btn_open.clicked.connect(self.cargar_excel)
        top_bar.addWidget(self.btn_open)

        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("🔍 Buscar por código, lote o producto...")
        self.txt_search.setFixedHeight(36)
        self.txt_search.setStyleSheet(
            "QLineEdit {"
            " border: 1px solid #CBD5E1;"
            " border-radius: 4px;"
            " padding: 0 12px;"
            " font-size: 11px;"
            " min-width: 240px;"
            " background-color: #FFFFFF;"
            "}"
            "QLineEdit:focus { border: 1px solid #1F4E79; }"
        )
        self.txt_search.textChanged.connect(self.filtrar_tabla)
        top_bar.addWidget(self.txt_search)

        self.lbl_info = QLabel("Ningún archivo Excel cargado.")
        self.lbl_info.setStyleSheet(
            "color: #555555; font-size: 11px; font-style: italic;"
        )
        top_bar.addWidget(self.lbl_info)

        top_bar.addStretch()

        self.btn_export_single = QPushButton("📄 Exportar Muestra Seleccionada")
        self.btn_export_single.setFixedHeight(38)
        self.btn_export_single.setEnabled(False)
        self.btn_export_single.setStyleSheet(
            "QPushButton {"
            " background-color: #1F4E79;"
            " color: #FFFFFF;"
            " font-size: 12px;"
            " font-weight: bold;"
            " border-radius: 4px;"
            " padding: 0 16px;"
            "}"
            "QPushButton:hover { background-color: #153755; }"
            "QPushButton:disabled { background-color: #E2E8F0; color: #94A3B8; }"
        )
        self.btn_export_single.clicked.connect(self.exportar_seleccionado)
        top_bar.addWidget(self.btn_export_single)

        self.btn_export_all = QPushButton("📑 Exportar Todos los Informes")
        self.btn_export_all.setFixedHeight(38)
        self.btn_export_all.setEnabled(False)
        self.btn_export_all.setStyleSheet(
            "QPushButton {"
            " background-color: #2E6930;"
            " color: #FFFFFF;"
            " font-size: 12px;"
            " font-weight: bold;"
            " border-radius: 4px;"
            " padding: 0 16px;"
            "}"
            "QPushButton:hover { background-color: #1E4620; }"
            "QPushButton:disabled { background-color: #E2E8F0; color: #94A3B8; }"
        )
        self.btn_export_all.clicked.connect(self.exportar_todos)
        top_bar.addWidget(self.btn_export_all)

        layout.addLayout(top_bar)

        # --- FILA 2: SELECTOR DE CARPETA DESTINO ---
        folder_bar = QHBoxLayout()
        folder_bar.setSpacing(8)

        lbl_dest = QLabel("📁 Carpeta de Guardado:")
        lbl_dest.setStyleSheet("font-weight: bold; color: #1E293B; font-size: 11px;")
        folder_bar.addWidget(lbl_dest)

        self.txt_folder = QLineEdit(self.output_directory)
        self.txt_folder.setFixedHeight(30)
        self.txt_folder.setReadOnly(True)
        self.txt_folder.setStyleSheet(
            "QLineEdit {"
            " background-color: #F1F5F9;"
            " border: 1px solid #CBD5E1;"
            " border-radius: 4px;"
            " padding: 0 8px;"
            " font-size: 11px;"
            " color: #334155;"
            "}"
        )
        folder_bar.addWidget(self.txt_folder)

        self.btn_change_folder = QPushButton("Seleccionar Carpeta...")
        self.btn_change_folder.setFixedHeight(30)
        self.btn_change_folder.setStyleSheet(
            "QPushButton {"
            " background-color: #475569;"
            " color: #FFFFFF;"
            " font-size: 11px;"
            " font-weight: bold;"
            " border-radius: 4px;"
            " padding: 0 12px;"
            "}"
            "QPushButton:hover { background-color: #334155; }"
        )
        self.btn_change_folder.clicked.connect(self.seleccionar_carpeta_destino)
        folder_bar.addWidget(self.btn_change_folder)

        self.btn_open_folder = QPushButton("Abrir Carpeta")
        self.btn_open_folder.setFixedHeight(30)
        self.btn_open_folder.setStyleSheet(
            "QPushButton {"
            " background-color: #E2E8F0;"
            " color: #0F172A;"
            " font-size: 11px;"
            " border: 1px solid #CBD5E1;"
            " border-radius: 4px;"
            " padding: 0 10px;"
            "}"
            "QPushButton:hover { background-color: #CBD5E1; }"
        )
        self.btn_open_folder.clicked.connect(self.abrir_carpeta_en_explorador)
        folder_bar.addWidget(self.btn_open_folder)

        layout.addLayout(folder_bar)

        # --- TABLA SIMPLIFICADA (1 FILA = 1 MUESTRA n=5) ---
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setStyleSheet(
            "QTableWidget {"
            " background-color: #FFFFFF;"
            " alternate-background-color: #F8FAFC;"
            " gridline-color: #E2E8F0;"
            " font-size: 11px;"
            " selection-background-color: #CBD5E1;"
            " selection-color: #000000;"
            " border: 1px solid #D1D5DB;"
            " border-radius: 4px;"
            "}"
            "QHeaderView::section {"
            " background-color: #002B49;"
            " color: #FFFFFF;"
            " font-weight: bold;"
            " font-size: 11px;"
            " padding: 7px 6px;"
            " border: 1px solid #002B49;"
            "}"
        )
        layout.addWidget(self.table)

        # --- BARRA DE PROGRESO ---
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setFixedHeight(12)
        self.progress_bar.setTextVisible(True)
        layout.addWidget(self.progress_bar)

        # --- STATUS BAR ---
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Listo. Abra un archivo Excel para comenzar.")

    def seleccionar_carpeta_destino(self):
        """Permite al usuario elegir la carpeta donde se guardarán los informes."""
        carpeta = QFileDialog.getExistingDirectory(
            self, "Seleccionar Carpeta para Guardar los Informes"
        )
        if carpeta:
            self.output_directory = os.path.join(carpeta, "informes_generados")
            self.txt_folder.setText(self.output_directory)
            self.status.showMessage(
                f"Carpeta de destino actualizada: {self.output_directory}", 5000
            )

    def abrir_carpeta_en_explorador(self):
        """Abre la carpeta en el Explorador de archivos del sistema."""
        os.makedirs(self.output_directory, exist_ok=True)
        if hasattr(os, "startfile"):
            os.startfile(self.output_directory)
        else:
            import subprocess

            subprocess.run(["xdg-open", self.output_directory])

    def cargar_excel(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Base de Datos Eurofins",
            "",
            "Archivos Excel (*.xlsx *.xls)",
        )
        if not file_path:
            return

        try:
            self.excel_file_path = file_path
            self.df_raw = pd.read_excel(file_path)

            excel_dir = os.path.dirname(os.path.abspath(file_path))
            self.output_directory = os.path.join(excel_dir, "informes_generados")
            self.txt_folder.setText(self.output_directory)

            self.construir_vista_muestras()
            self.poblar_tabla()

            self.btn_export_single.setEnabled(True)
            self.btn_export_all.setEnabled(True)

            total_muestras = len(self.df_samples)
            self.lbl_info.setText(
                f"Archivo: {os.path.basename(file_path)} | Muestras (n=5):"
                f" {total_muestras}"
            )
            self.status.showMessage(
                f"Base de datos cargada: {total_muestras} muestras disponibles para"
                " generar.",
                6000,
            )
        except Exception as e:
            QMessageBox.critical(
                self, "Error al Cargar Excel", f"Detalle del error:\n{str(e)}"
            )

    def construir_vista_muestras(self):
        col_code = "Sample Code (Eurofins)"
        if col_code not in self.df_raw.columns:
            col_code = self.df_raw.columns[0]

        muestras_lista = []
        grupos = self.df_raw.groupby(col_code, sort=False)

        for sample_code, group in grupos:
            first = group.iloc[0]

            if "ID Muestra (CUST)" in group.columns:
                n_val = group["ID Muestra (CUST)"].nunique()
            else:
                n_val = 5

            dictamen = first.get(
                "Estado / Dictamen",
                first.get("Dictamen", first.get("Estado", "Conforme")),
            )

            muestras_lista.append(
                {
                    "Código Muestra": str(sample_code).strip(),
                    "Nº Informe (AR)": str(
                        first.get("Informe Analítico (AR)", first.get("AR", ""))
                    ).strip(),
                    "Lote / Ref. Cliente": str(
                        first.get("Ref. Cliente (Lote/Exp)", "")
                    ).strip(),
                    "Producto / Muestra": str(
                        first.get("Producto / Muestra", "")
                    ).strip(),
                    "Fecha Informe": str(first.get("Fecha Informe", "")).strip(),
                    "Semana": str(first.get("Semana", "")).strip(),
                    "Sección": str(first.get("Sección", "")).strip(),
                    "Determinaciones": f"n = {n_val} (CUST 01-0{n_val})",
                    "Estado": str(dictamen).strip(),
                }
            )

        self.df_samples = pd.DataFrame(muestras_lista)

    def poblar_tabla(self):
        self.table.clear()
        self.table.setRowCount(len(self.df_samples))
        self.table.setColumnCount(len(self.df_samples.columns))
        self.table.setHorizontalHeaderLabels([str(c) for c in self.df_samples.columns])

        for row_idx in range(len(self.df_samples)):
            for col_idx in range(len(self.df_samples.columns)):
                val = self.df_samples.iat[row_idx, col_idx]
                item = QTableWidgetItem("" if pd.isna(val) else str(val))

                col_name = str(self.df_samples.columns[col_idx])
                if any(
                    k in col_name
                    for k in [
                        "Código",
                        "Nº",
                        "Fecha",
                        "Semana",
                        "Determinaciones",
                        "Lote",
                    ]
                ):
                    item.setTextAlignment(Qt.AlignCenter)
                elif "Estado" in col_name or "Dictamen" in col_name:
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setForeground(QColor("#276A3C"))
                    item.setFont(QFont("Calibri", 10, QFont.Bold))
                else:
                    item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

                self.table.setItem(row_idx, col_idx, item)

        self.table.resizeColumnsToContents()

    def filtrar_tabla(self):
        filtro = self.txt_search.text().lower()
        for row in range(self.table.rowCount()):
            coincide = False
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and filtro in item.text().lower():
                    coincide = True
                    break
            self.table.setRowHidden(row, not coincide)

    def exportar_seleccionado(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(
                self, "Aviso", "Seleccione una muestra en la tabla para generarla."
            )
            return

        sample_code = self.table.item(current_row, 0).text().strip()

        col_code = "Sample Code (Eurofins)"
        if col_code not in self.df_raw.columns:
            col_code = self.df_raw.columns[0]

        muestras_grupo = self.df_raw[
            self.df_raw[col_code].astype(str).str.strip() == sample_code
        ].to_dict(orient="records")

        if not muestras_grupo:
            QMessageBox.warning(
                self, "Aviso", "No se encontraron ensayos para la muestra."
            )
            return

        os.makedirs(self.output_directory, exist_ok=True)

        filename = get_official_filename(muestras_grupo[0])
        out_pdf = os.path.join(self.output_directory, filename)

        try:
            self.status.showMessage(f"Generando informe oficial {filename}...")
            QApplication.processEvents()
            pdf_generator.build_eurofins_clone_pdf(muestras_grupo, out_pdf)
            self.status.showMessage(f"Informe generado con éxito: {filename}", 6000)

            if hasattr(os, "startfile"):
                os.startfile(self.output_directory)

            QMessageBox.information(
                self,
                "Informe Completado",
                "Se ha generado exitosamente el informe de 3 páginas"
                f" (n=5):\n\n{filename}\n\nGuardado en:\n{self.output_directory}",
            )
        except Exception as e:
            QMessageBox.critical(
                self, "Error al Generar PDF", f"Detalle del error:\n{str(e)}"
            )

    def exportar_todos(self):
        if self.df_raw is None or len(self.df_raw) == 0:
            return

        os.makedirs(self.output_directory, exist_ok=True)

        col_code = "Sample Code (Eurofins)"
        if col_code not in self.df_raw.columns:
            col_code = self.df_raw.columns[0]

        grupos = self.df_raw.groupby(col_code, sort=False)
        total_muestras = len(grupos)

        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, total_muestras)
        self.progress_bar.setValue(0)

        count = 0
        errores = []

        for sample_code, group in grupos:
            muestras_lote = group.to_dict(orient="records")
            filename = get_official_filename(muestras_lote[0])
            out_pdf = os.path.join(self.output_directory, filename)

            try:
                pdf_generator.build_eurofins_clone_pdf(muestras_lote, out_pdf)
            except Exception as err:
                errores.append(f"{filename}: {str(err)}")

            count += 1
            self.progress_bar.setValue(count)
            self.status.showMessage(
                f"Generando informes oficiales... ({count}/{total_muestras})"
            )
            QApplication.processEvents()

        self.progress_bar.setVisible(False)

        if errores:
            msg = (
                f"Se generaron {count - len(errores)} de {total_muestras} informes.\n"
                f"Hubo {len(errores)} errores:\n" + "\n".join(errores[:3])
            )
            QMessageBox.warning(self, "Finalizado con Errores", msg)
        else:
            self.status.showMessage(
                f"Generación completada: {total_muestras} informes oficiales listos.",
                7000,
            )

            if hasattr(os, "startfile"):
                os.startfile(self.output_directory)

            QMessageBox.information(
                self,
                "Exportación Finalizada",
                f"Se han generado los {total_muestras} informes oficiales de 3 páginas"
                f" en:\n{self.output_directory}",
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EurofinsReportApp()
    window.show()
    sys.exit(app.exec_())
