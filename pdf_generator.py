import sys
import os
from reportlab.graphics.barcode import code128
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    Image as RLImage,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


def resolver_ruta_asset(nombre_archivo, base_dir):
    """Busca la imagen en la carpeta temporal del .exe, en ./assets o en la raíz."""
    # Ruta temporal si se ejecuta empaquetado con PyInstaller
    base_exe = getattr(sys, "_MEIPASS", base_dir)

    posibles_rutas = [
        os.path.join(base_exe, "assets", nombre_archivo),
        os.path.join(base_exe, nombre_archivo),
        os.path.join(base_dir, "assets", nombre_archivo),
        os.path.join(base_dir, nombre_archivo),
        os.path.join(os.getcwd(), "assets", nombre_archivo),
        os.path.join(os.getcwd(), nombre_archivo),
    ]
    for r in posibles_rutas:
        if os.path.exists(r):
            return os.path.abspath(r)
    return os.path.join(base_dir, "assets", nombre_archivo)


def build_eurofins_clone_pdf(muestras_list, output_pdf_path):
    if not isinstance(muestras_list, list):
        muestras_list = [muestras_list]

    first = muestras_list[0]
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Resolución dinámica y segura de las 3 imágenes
    logo_hdr_path = resolver_ruta_asset("eurofins_header_logo.png", base_dir)
    logo_enac_path = resolver_ruta_asset("enac_ilac_oficial.png", base_dir)
    firma_completa_path = resolver_ruta_asset("firma_completa_nuria.png", base_dir)

    # Configuración del documento con margen inferior reservado para el pie fijo
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        leftMargin=26.75,
        rightMargin=26.75,
        topMargin=20,
        bottomMargin=84,  # Reserva espacio para el pie en y = 14..78 pt
    )

    styles = getSampleStyleSheet()
    normal = styles["Normal"]

    # Tipografías oficiales
    f_title = ParagraphStyle(
        "TitleExact",
        parent=normal,
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=12,
        textColor=colors.black,
    )
    b_lbl = ParagraphStyle(
        "BLbl",
        parent=normal,
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=colors.black,
    )
    b_val = ParagraphStyle(
        "BVal",
        parent=normal,
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=colors.black,
    )
    b_page = ParagraphStyle(
        "BPage",
        parent=normal,
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=colors.black,
        alignment=2,
    )

    cli_name = ParagraphStyle(
        "CliName",
        parent=normal,
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=colors.black,
    )
    attn_lbl = ParagraphStyle(
        "AttnLbl",
        parent=normal,
        fontName="Helvetica",
        fontSize=7.2,
        leading=9,
        textColor=colors.black,
        alignment=2,
    )
    attn_val = ParagraphStyle(
        "AttnVal",
        parent=normal,
        fontName="Helvetica-Bold",
        fontSize=7.2,
        leading=9,
        textColor=colors.black,
    )
    addr_text = ParagraphStyle(
        "AddrText",
        parent=normal,
        fontName="Helvetica",
        fontSize=7.2,
        leading=9,
        textColor=colors.black,
    )

    m_lbl = ParagraphStyle(
        "MLbl",
        parent=normal,
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=9.5,
        textColor=colors.black,
    )
    m_val = ParagraphStyle(
        "MVal",
        parent=normal,
        fontName="Helvetica",
        fontSize=7.5,
        leading=9.5,
        textColor=colors.black,
    )
    disclaimer_style = ParagraphStyle(
        "Disc",
        parent=normal,
        fontName="Helvetica",
        fontSize=6.2,
        leading=7.8,
        textColor=colors.black,
    )

    c_lbl = ParagraphStyle(
        "CLbl",
        parent=normal,
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=9.5,
        textColor=colors.black,
    )
    c_val = ParagraphStyle(
        "CVal",
        parent=normal,
        fontName="Helvetica",
        fontSize=7.5,
        leading=9.5,
        textColor=colors.black,
    )
    c_val_b = ParagraphStyle(
        "CValB",
        parent=normal,
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=9.5,
        textColor=colors.black,
    )

    micro_hdr_left = ParagraphStyle(
        "MHLeft",
        parent=normal,
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=9.5,
        textColor=colors.black,
    )
    micro_hdr_right = ParagraphStyle(
        "MHRight",
        parent=normal,
        fontName="Helvetica",
        fontSize=7.5,
        leading=9.5,
        textColor=colors.black,
        alignment=0,
    )
    cust_title = ParagraphStyle(
        "CustT",
        parent=normal,
        fontName="Helvetica-Bold",
        fontSize=7.2,
        leading=9,
        textColor=colors.black,
    )

    test_line1 = ParagraphStyle(
        "TLine1",
        parent=normal,
        fontName="Helvetica-Bold",
        fontSize=6.2,
        leading=7.8,
        textColor=colors.black,
    )
    test_param = ParagraphStyle(
        "TParam",
        parent=normal,
        fontName="Helvetica",
        fontSize=6.5,
        leading=8.2,
        textColor=colors.black,
        leftIndent=26,
    )
    test_result = ParagraphStyle(
        "TRes",
        parent=normal,
        fontName="Helvetica",
        fontSize=6.5,
        leading=8.2,
        textColor=colors.black,
    )

    sig_lbl_top = ParagraphStyle(
        "SigLblTop",
        parent=normal,
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=9.5,
        textColor=colors.black,
    )
    sig_disc = ParagraphStyle(
        "SigDisc",
        parent=normal,
        fontName="Helvetica",
        fontSize=6.5,
        leading=8.5,
        textColor=colors.black,
    )

    exp_title = ParagraphStyle(
        "ExpTitle",
        parent=normal,
        fontName="Helvetica-Bold",
        fontSize=7.8,
        leading=10,
        textColor=colors.black,
    )
    exp_body = ParagraphStyle(
        "ExpBody",
        parent=normal,
        fontName="Helvetica",
        fontSize=6.8,
        leading=9.2,
        textColor=colors.black,
    )
    exp_body_indent = ParagraphStyle(
        "ExpBodyIndent",
        parent=normal,
        fontName="Helvetica",
        fontSize=6.8,
        leading=9.2,
        textColor=colors.black,
        leftIndent=12,
    )

    ft_texto_r = ParagraphStyle(
        "FTTexto",
        parent=normal,
        fontName="Helvetica",
        fontSize=6.2,
        leading=8,
        textColor=colors.black,
    )
    ft_disclaimer = ParagraphStyle(
        "FTDisc",
        parent=normal,
        fontName="Helvetica",
        fontSize=6.2,
        leading=8,
        textColor=colors.black,
        alignment=2,
    )

    # -------------------------------------------------------------
    # DIBUJO DEL PIE ANCLADO AL FONDO (EN LAS 3 PÁGINAS)
    # -------------------------------------------------------------
    col1_html = (
        "<b>Eurofins Análisis Alimentario, S.L.U.</b><br/>AV. INDUSTRIA NUM."
        " 13,<br/>28823 Coslada<br/><b>SPAIN</b>"
    )
    col2_html = (
        "Phone &nbsp;&nbsp;&nbsp; +34 912 756 386<br/>Fax"
        " &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        " +34910900825<br/>foodtestingmadrid@ftib.eurofins.com<br/>https://www.eurofins.com/food-and-feed-tes<br/>ting/"
    )
    col3_html = (
        "Registro Mercantil de Barcelona,<br/>Tomo 44128, Folio 145,<br/>Hoja B"
        " 447479, Inscripción 1.<br/>CIF B-66198391"
    )

    enac_element = (
        RLImage(logo_enac_path, width=74, height=44)
        if os.path.exists(logo_enac_path)
        else ""
    )

    footer_table = Table(
        [
            [
                Paragraph(col1_html, ft_texto_r),
                Paragraph(col2_html, ft_texto_r),
                Paragraph(col3_html, ft_texto_r),
                enac_element,
            ],
            [
                "",
                "",
                Paragraph(
                    "(*) Tests and marked activities are not covered by the ENAC"
                    " accreditation.",
                    ft_disclaimer,
                ),
                "",
            ],
        ],
        colWidths=[140, 160, 160, 81.5],
    )
    footer_table.setStyle(
        TableStyle(
            [
                ("SPAN", (2, 1), (3, 1)),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 2),
                ("TOPPADDING", (0, 1), (-1, 1), 2),
            ]
        )
    )
    footer_table.wrap(541.5, 80)

    def draw_footer_callback(canvas, document):
        canvas.saveState()
        footer_table.drawOn(canvas, 26.75, 14)
        canvas.restoreState()

    story = []

    # =========================================================================
    # PÁGINA 1
    # =========================================================================
    hdr_logo_p1 = (
        RLImage(logo_hdr_path, width=220, height=48)
        if os.path.exists(logo_hdr_path)
        else ""
    )
    t_top_p1 = Table(
        [[hdr_logo_p1, Paragraph("Analytical report", f_title)]],
        colWidths=[355, 186.5],
    )
    t_top_p1.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
                ("BOTTOMPADDING", (1, 0), (1, 0), 6),
                ("PADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    story.append(t_top_p1)
    story.append(Spacer(1, 3))

    sample_code_val = str(first.get("Sample Code (Eurofins)", "386-2026-00096020"))
    rep_date_val = str(first.get("Fecha Informe", "10/08/2026"))
    ar_nr_val = (
        f"{first.get('Informe Analítico (AR)', 'AR-26-AQ-091946-01')} /"
        f" {sample_code_val}"
    )

    t_line1_p1 = Table(
        [
            [
                Paragraph("Sample code Nr.", b_lbl),
                Paragraph(sample_code_val, b_val),
                Paragraph("Report Date", b_lbl),
                Paragraph(rep_date_val, b_val),
                Paragraph("Page 1/3", b_page),
            ]
        ],
        colWidths=[142, 148, 72, 108, 71.5],
    )
    t_line1_p1.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("PADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )

    t_line2_p1 = Table(
        [
            [
                Paragraph("Analytical Report Nr.", b_lbl),
                Paragraph(ar_nr_val, b_val),
            ]
        ],
        colWidths=[168, 373.5],
    )
    t_line2_p1.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("PADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )

    t_box_p1 = Table([[t_line1_p1], [t_line2_p1]], colWidths=[541.5])
    t_box_p1.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 1.0, colors.black),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 2.5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(t_box_p1)
    story.append(Spacer(1, 4))

    barcode_compact = code128.Code128(
        sample_code_val, barHeight=7.5, barWidth=0.40, humanReadable=False
    )
    nom_cli = (
        str(
            first.get("Nombre Cliente", "INCARLOPSA EXPORTACION (FRESCO.-EXP.)")
        ).strip()
        or "INCARLOPSA EXPORTACION (FRESCO.-EXP.)"
    )
    attn_cli = (
        str(
            first.get(
                "Atención (Persona / Dpto)",
                "CALIDAD EXPORTACION CALIDAD\nEXPORTACION",
            )
        )
        .strip()
        .replace("\n", "<br/>")
    )
    dir_cli = (
        str(
            first.get(
                "Dirección Cliente",
                "Ctra. N-400, Km. 95,4\n16400 Tarancón\nESPAÑA",
            )
        )
        .strip()
        .replace("\n", "<br/>")
    )

    client_data = [
        [barcode_compact, "", Paragraph(nom_cli, cli_name)],
        [
            "",
            Paragraph("For the attention of", attn_lbl),
            Paragraph(attn_cli, attn_val),
        ],
        ["", "", Paragraph(dir_cli, addr_text)],
    ]
    t_client = Table(client_data, colWidths=[208, 80, 253.5])
    t_client.setStyle(
        TableStyle(
            [
                ("SPAN", (0, 0), (0, 2)),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 0.5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0.5),
                ("PADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    story.append(t_client)
    story.append(Spacer(1, 4))

    desc_val = str(
        first.get(
            "Sample description",
            "Carne y productos derivados / Meat and derived products",
        )
    )
    recep_date_val = str(first.get("Fecha Recepción", "06/08/2026"))
    start_date_val = str(
        first.get("Fecha Inicio Análisis", first.get("Fecha Recepción", ""))
    )
    end_date_val = str(first.get("Fecha Fin Análisis", first.get("Fecha Informe", "")))
    temp_val = str(first.get("Temp. Recepción", "CONG"))

    sample_box_data = [
        [
            Paragraph("Sample description", m_lbl),
            Paragraph(desc_val, m_val),
            "",
            "",
        ],
        [
            Paragraph("Sample reception date :", m_lbl),
            Paragraph(recep_date_val, m_val),
            "",
            "",
        ],
        [
            Paragraph("Analysis starting date :", m_lbl),
            Paragraph(start_date_val, m_val),
            Paragraph("Analysis end date:", m_lbl),
            Paragraph(end_date_val, m_val),
        ],
        [
            Paragraph("Sampling/Transport :", m_lbl),
            Paragraph("*Recogido/toma muestra Eurofins", m_val),
            Paragraph("* Reception temperature (&ordm;C) :", m_lbl),
            Paragraph(temp_val, m_val),
        ],
    ]
    t_sample_box = Table(sample_box_data, colWidths=[130, 145, 145, 121.5])
    t_sample_box.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 1.0, colors.black),
                ("SPAN", (1, 0), (3, 0)),
                ("SPAN", (1, 1), (3, 1)),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 1.8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1.8),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(t_sample_box)
    story.append(Spacer(1, 2.5))

    disclaimer_text = (
        "The information in the table below has been provided by the client and"
        " the laboratory is not responsible for it. This information is not"
        " covered by accreditation."
    )
    story.append(Paragraph(disclaimer_text, disclaimer_style))
    story.append(Spacer(1, 2.5))

    ref_cli = str(first.get("Ref. Cliente (Lote/Exp)", "EXP_0407"))
    ref_sample = str(first.get("Producto / Muestra", "DIAFRAGMA /"))
    comm_val = str(first.get("Comments", "Sample size>500g"))
    sem_val = str(first.get("Semana", "32"))
    paq_val = str(first.get("Paquete Análisis", "China + Corea+Malasia (verde)"))
    sec_val = str(first.get("Sección", "TRIPERIA_PORCINO/CASING_ROOM"))
    subsec_val = str(first.get("Subsección", "SALA_VÍSCERAS_ROJAS/RED_CASING_ROOM"))
    samp_date_val = str(first.get("Fecha Toma Muestra", "2026-08-06"))

    client_tracking_data = [
        [Paragraph("Client reference", c_lbl), Paragraph(ref_cli, c_val_b), "", ""],
        [
            Paragraph("Sample reference", c_lbl),
            Paragraph(ref_sample, c_val),
            "",
            "",
        ],
        [
            Paragraph("Comments", c_lbl),
            Paragraph(comm_val, c_val),
            Paragraph("Sample taking date<br/>(client)", c_lbl),
            Paragraph(recep_date_val, c_val),
        ],
        [
            Paragraph("Semana", c_lbl),
            Paragraph(sem_val, c_val),
            Paragraph("Paquete analisis", c_lbl),
            Paragraph(paq_val, c_val),
        ],
        [
            Paragraph("Seccion", c_lbl),
            Paragraph(sec_val, c_val),
            Paragraph("Subseccion", c_lbl),
            Paragraph(subsec_val, c_val),
        ],
        [
            Paragraph("Sampling date :", c_lbl),
            Paragraph(samp_date_val, c_val),
            "",
            "",
        ],
    ]
    t_client_tracking = Table(client_tracking_data, colWidths=[130, 145, 125, 141.5])
    t_client_tracking.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 1.0, colors.black),
                ("LINEBELOW", (0, 0), (-1, -2), 0.5, colors.HexColor("#D0D0D0")),
                ("SPAN", (1, 0), (3, 0)),
                ("SPAN", (1, 1), (3, 1)),
                ("SPAN", (1, 5), (3, 5)),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 1.5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(t_client_tracking)
    story.append(Spacer(1, 3))

    # Microbiológico P1: CUST 01 y CUST 02
    micro_rows_p1 = [
        [
            Paragraph("Microbiological analysis", micro_hdr_left),
            Paragraph("Results", micro_hdr_right),
        ]
    ]

    def get_subsample_tests(row_item):
        return [
            {
                "code": "UM2AD",
                "method": (
                    "AQ Enterobacteriaceae E &lt;10 &gt;15000 /g (1-2) PEB-PF AFNOR"
                    " 3M 01/06-09/97 &nbsp;&nbsp;&nbsp;&nbsp; Method : AL-TM3347"
                    " (Recuento en placa:EB)"
                ),
                "name": "Enterobacteriaceae",
                "result": f"{row_item.get('Enterobacteriaceae (cfu/g)', '-')} cfu/g",
            },
            {
                "code": "UMM6J",
                "method": (
                    "AQ Coliforms E &lt;100 &gt;150000 /g (2-3) PCC-PF AFNOR 3M"
                    " 01/02-09/89A &nbsp;&nbsp;&nbsp;&nbsp; Method : AL-TM3365"
                    " (Recuento en placa:CC)"
                ),
                "name": "Coliforms",
                "result": f"{row_item.get('Coliformes Totales (cfu/g)', '-')} cfu/g",
            },
            {
                "code": "UMSA0",
                "method": (
                    "AQ Escherichia coli B-Glucuronidase+ E &lt;10 &gt;15000 /g"
                    " (1-2) PSEC-PF AFNOR 3M 01/08-06/01 &nbsp;&nbsp;&nbsp;&nbsp;"
                    " Method : AL-TM3355<br/>(Recuento en placa:SEC)"
                ),
                "name": "Escherichia coli B-Glucuronidase+",
                "result": f"{row_item.get('Escherichia coli (cfu/g)', '-')} cfu/g",
            },
            {
                "code": "UMWIS",
                "method": (
                    "AQ Aerobic plate count E &lt;1000 &gt;3000000 /g (3-4) PAC-PF"
                    " AFNOR 3M 01/01-09/89-M &nbsp;&nbsp;&nbsp;&nbsp; Method :"
                    " AL-TM3346 (Recuento en<br/>placa:AC)"
                ),
                "name": "Aerobic Plate Count",
                "result": (
                    f"{row_item.get('Recuento Aerobios Mesófilos (cfu/g)', '-')} cfu/g"
                ),
            },
            {
                "code": "UMYUT",
                "method": (
                    "AQ Salmonella D Abs Pres /25 g AFNOR BRD 07/11-12/05"
                    " &nbsp;&nbsp;&nbsp;&nbsp; Method : AL-TM4865 (Detección en"
                    " placa: RSLM)"
                ),
                "name": "Salmonella",
                "result": f"{row_item.get('Salmonella (/25g)', 'Not Detected')} /25 g",
            },
        ]

    def add_subsample(rows, cust_label, test_list):
        rows.append([Paragraph(f"<b>Analyses on:{cust_label}</b>", cust_title), ""])
        for item in test_list:
            full_method = f"<b>{item['code']} &nbsp;&nbsp; {item['method']}</b>"
            rows.append([Paragraph(full_method, test_line1), ""])
            rows.append(
                [
                    Paragraph(item["name"], test_param),
                    Paragraph(item["result"], test_result),
                ]
            )

    is_relational = "Código Método" in first
    if is_relational:
        from collections import OrderedDict

        grouped_cust = OrderedDict()
        for r in muestras_list:
            cid = str(r.get("ID Muestra (CUST)", "CUST 01"))
            if cid not in grouped_cust:
                grouped_cust[cid] = []
            grouped_cust[cid].append(
                {
                    "code": str(r.get("Código Método", "")),
                    "method": str(r.get("Método", "")),
                    "name": str(r.get("Nombre Parámetro", "")),
                    "result": (
                        f"{r.get('Resultado', '')} {r.get('Unidades', '')}".strip()
                    ),
                }
            )
        for cid, tlist in list(grouped_cust.items())[:2]:
            add_subsample(micro_rows_p1, cid, tlist)
    else:
        add_subsample(
            micro_rows_p1,
            muestras_list[0].get("ID Muestra (CUST)", "CUST 01"),
            get_subsample_tests(muestras_list[0]),
        )
        if len(muestras_list) > 1:
            add_subsample(
                micro_rows_p1,
                muestras_list[1].get("ID Muestra (CUST)", "CUST 02"),
                get_subsample_tests(muestras_list[1]),
            )

    micro_rows_p1.append([Paragraph("<b>Analyses on:CUST 03</b>", cust_title), ""])

    t_styles = [
        ("BOX", (0, 0), (-1, -1), 1.0, colors.black),
        ("LINEBELOW", (0, 0), (-1, 0), 1.0, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 0.6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0.6),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]
    t_styles.append(("SPAN", (0, 1), (1, 1)))
    for i in [2, 4, 6, 8, 10]:
        t_styles.append(("SPAN", (0, i), (1, i)))
    t_styles.append(("SPAN", (0, 12), (1, 12)))
    for i in [13, 15, 17, 19, 21]:
        t_styles.append(("SPAN", (0, i), (1, i)))
    t_styles.append(("SPAN", (0, 23), (1, 23)))

    t_micro_p1 = Table(micro_rows_p1, colWidths=[285, 256.5])
    t_micro_p1.setStyle(TableStyle(t_styles))
    story.append(t_micro_p1)

    # =========================================================================
    # PÁGINA 2
    # =========================================================================
    story.append(PageBreak())

    hdr_logo_p2 = (
        RLImage(logo_hdr_path, width=220, height=48)
        if os.path.exists(logo_hdr_path)
        else ""
    )
    t_top_p2 = Table(
        [[hdr_logo_p2, Paragraph("Analytical report", f_title)]],
        colWidths=[355, 186.5],
    )
    t_top_p2.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
                ("BOTTOMPADDING", (1, 0), (1, 0), 6),
                ("PADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    story.append(t_top_p2)
    story.append(Spacer(1, 3))

    t_line1_p2 = Table(
        [
            [
                Paragraph("Sample code Nr.", b_lbl),
                Paragraph(sample_code_val, b_val),
                Paragraph("Report Date", b_lbl),
                Paragraph(rep_date_val, b_val),
                Paragraph("Page 2/3", b_page),
            ]
        ],
        colWidths=[142, 148, 72, 108, 71.5],
    )
    t_line1_p2.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("PADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )

    t_line2_p2 = Table(
        [
            [
                Paragraph("Analytical Report Nr.", b_lbl),
                Paragraph(ar_nr_val, b_val),
            ]
        ],
        colWidths=[168, 373.5],
    )
    t_line2_p2.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("PADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )

    t_box_p2 = Table([[t_line1_p2], [t_line2_p2]], colWidths=[541.5])
    t_box_p2.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 1.0, colors.black),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 2.5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(t_box_p2)
    story.append(Spacer(1, 4))

    micro_rows_p2 = [
        [
            Paragraph("Microbiological analysis", micro_hdr_left),
            Paragraph("Results", micro_hdr_right),
        ]
    ]

    if is_relational:
        for cid, tlist in list(grouped_cust.items())[2:]:
            add_subsample(micro_rows_p2, cid, tlist)
    else:
        for cust_idx in range(2, len(muestras_list)):
            row_c = muestras_list[cust_idx]
            add_subsample(
                micro_rows_p2,
                row_c.get("ID Muestra (CUST)", f"CUST 0{cust_idx+1}"),
                get_subsample_tests(row_c),
            )

    t_styles_p2 = [
        ("BOX", (0, 0), (-1, -1), 1.0, colors.black),
        ("LINEBELOW", (0, 0), (-1, 0), 1.0, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 0.6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0.6),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]
    t_styles_p2.append(("SPAN", (0, 1), (1, 1)))
    for i in [2, 4, 6, 8, 10]:
        t_styles_p2.append(("SPAN", (0, i), (1, i)))
    t_styles_p2.append(("SPAN", (0, 12), (1, 12)))
    for i in [13, 15, 17, 19, 21]:
        t_styles_p2.append(("SPAN", (0, i), (1, i)))
    t_styles_p2.append(("SPAN", (0, 23), (1, 23)))
    for i in [24, 26, 28, 30, 32]:
        t_styles_p2.append(("SPAN", (0, i), (1, i)))

    t_micro_p2 = Table(micro_rows_p2, colWidths=[285, 256.5])
    t_micro_p2.setStyle(TableStyle(t_styles_p2))
    story.append(t_micro_p2)
    story.append(Spacer(1, 5))

    firma_element = (
        RLImage(firma_completa_path, width=185, height=46)
        if os.path.exists(firma_completa_path)
        else ""
    )
    sig_table_data = [[Paragraph("<b>SIGNATURE</b>", sig_lbl_top), firma_element]]
    t_sig_box = Table(sig_table_data, colWidths=[90, 451.5])
    t_sig_box.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 1.0, colors.black),
                ("VALIGN", (0, 0), (0, 0), "TOP"),
                ("VALIGN", (1, 0), (1, 0), "MIDDLE"),
                ("ALIGN", (1, 0), (1, 0), "LEFT"),
                ("LEFTPADDING", (1, 0), (1, 0), 30),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("LEFTPADDING", (0, 0), (0, 0), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(t_sig_box)
    story.append(Spacer(1, 3))

    story.append(
        Paragraph(
            "Microbiology validated by Nuria Nieto<br/>Report electronically"
            " validated by Nuria Nieto",
            sig_disc,
        )
    )

    # =========================================================================
    # PÁGINA 3: EXPLANATORY NOTE
    # =========================================================================
    story.append(PageBreak())

    hdr_logo_p3 = (
        RLImage(logo_hdr_path, width=220, height=48)
        if os.path.exists(logo_hdr_path)
        else ""
    )
    t_top_p3 = Table(
        [[hdr_logo_p3, Paragraph("Analytical report", f_title)]],
        colWidths=[355, 186.5],
    )
    t_top_p3.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
                ("BOTTOMPADDING", (1, 0), (1, 0), 6),
                ("PADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    story.append(t_top_p3)
    story.append(Spacer(1, 3))

    t_line1_p3 = Table(
        [
            [
                Paragraph("Sample code Nr.", b_lbl),
                Paragraph(sample_code_val, b_val),
                Paragraph("Report Date", b_lbl),
                Paragraph(rep_date_val, b_val),
                Paragraph("Page 3/3", b_page),
            ]
        ],
        colWidths=[142, 148, 72, 108, 71.5],
    )
    t_line1_p3.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("PADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )

    t_line2_p3 = Table(
        [
            [
                Paragraph("Analytical Report Nr.", b_lbl),
                Paragraph(ar_nr_val, b_val),
            ]
        ],
        colWidths=[168, 373.5],
    )
    t_line2_p3.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("PADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )

    t_box_p3 = Table([[t_line1_p3], [t_line2_p3]], colWidths=[541.5])
    t_box_p3.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 1.0, colors.black),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 2.5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(t_box_p3)
    story.append(Spacer(1, 6))

    exp_note_text = [
        Paragraph("<b>EXPLANATORY NOTE</b>", exp_title),
        Spacer(1, 3),
        Paragraph(
            "This document can only be reproduced in full ; it only concerns the"
            " submitted sample.",
            exp_body,
        ),
        Paragraph(
            "When the laboratory has not been responsible for sampling, the"
            " results are applied to the sample as received.",
            exp_body,
        ),
        Paragraph(
            "Results have been obtained and reported in accordance with our"
            " general sales conditions available on request.",
            exp_body,
        ),
        Spacer(1, 8),
        Paragraph(
            "Only results for which a specification or a standard is quoted are"
            " taken into account during interpretation.",
            exp_body,
        ),
        Paragraph(
            "In order to declare conformity to existing regulations or customer"
            " specifications, the uncertainty associated with the result will be"
            " added or<br/>removed in such a way that the result can be"
            " interpreted in any case regarding the specifications or regulations"
            " in force. It will not be taken into<br/>account in case of"
            " standards which already incorporate the measurement uncertainties.",
            exp_body,
        ),
        Paragraph(
            "The uncertainties of the results have been calculated (for K=2, with"
            " a coverage probability of 95%), and are available to the customer.",
            exp_body,
        ),
        Paragraph(
            "The tests are identified by a five-digit code, their description is"
            " available on request.",
            exp_body,
        ),
        Paragraph("Abbreviations:", exp_body),
        Paragraph("ND: Not detected", exp_body_indent),
        Paragraph(
            'NE: The term "estimated number" means a less accurate estimate of the'
            " true value.",
            exp_body_indent,
        ),
        Spacer(1, 8),
        Paragraph(
            "The tests identified by the two letters code AQ are performed in"
            " laboratory Eurofins Análisis Alimentario, S.L.U..",
            exp_body,
        ),
    ]

    t_exp_box = Table([[exp_note_text]], colWidths=[541.5])
    t_exp_box.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 1.0, colors.black),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(t_exp_box)

    # Compilación fijando el pie al fondo en cada página
    doc.build(
        story, onFirstPage=draw_footer_callback, onLaterPages=draw_footer_callback
    )
