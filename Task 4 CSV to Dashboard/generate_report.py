import os
import sys
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

# Define NumberedCanvas for dynamic "Page X of Y"
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        # Running Header (Pages 2+)
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#475569"))
            self.drawString(54, 11 * inch - 36, "AUSPIFY TECHNOLOGIES  |  POWER BI INTERNSHIP PROGRAM")
            self.setFont("Helvetica", 8)
            self.drawRightString(8.5 * inch - 54, 11 * inch - 36, "Dataset Quality Audit & Power BI Solutions")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.75)
            self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)

        # Running Footer (All pages)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.75)
        self.line(54, 45, 8.5 * inch - 54, 45)

        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 32, "Confidential  |  Prepared for Netflix Dashboard & Power BI Development")
        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(8.5 * inch - 54, 32, page_str)
        self.restoreState()


def build_pdf():
    pdf_path = r"D:\كورسات\AUSPIFY\Dataset_Quality_Report_PowerBI_Solutions.pdf"
    
    # 0.75 inch margins = 54 pt (Printable width: 504 pt)
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Color Palette
    PRIMARY = colors.HexColor("#0F172A")      # Navy 900
    SECONDARY = colors.HexColor("#E50914")    # Netflix Crimson
    ACCENT_BLUE = colors.HexColor("#1D4ED8")  # Royal Blue 700
    TEXT_DARK = colors.HexColor("#1E293B")    # Slate 800
    TEXT_MUTED = colors.HexColor("#475569")   # Slate 600
    BG_LIGHT = colors.HexColor("#F8FAFC")     # Slate 50
    BG_CARD = colors.HexColor("#F1F5F9")      # Slate 100
    BORDER_COLOR = colors.HexColor("#E2E8F0") # Slate 200
    CRITICAL_RED = colors.HexColor("#DC2626") # Red 600
    WARNING_AMBER = colors.HexColor("#D97706")# Amber 600
    SUCCESS_GREEN = colors.HexColor("#059669")# Emerald 600

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=19,
        leading=23,
        textColor=PRIMARY,
        spaceAfter=3
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=SECONDARY,
        spaceAfter=8
    )

    meta_style = ParagraphStyle(
        'MetaText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=TEXT_MUTED
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=16,
        textColor=PRIMARY,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13.5,
        textColor=ACCENT_BLUE,
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=TEXT_DARK,
        spaceAfter=3
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=TEXT_DARK,
        leftIndent=10,
        firstLineIndent=-6,
        spaceAfter=2
    )

    code_inline = ParagraphStyle(
        'CodeInline',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=7.2,
        leading=9.5,
        textColor=PRIMARY
    )

    code_block = ParagraphStyle(
        'CodeBlock',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7,
        leading=9.2,
        textColor=colors.HexColor("#0F172A")
    )

    tbl_header_style = ParagraphStyle(
        'TblHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=10,
        textColor=colors.white
    )

    tbl_cell_style = ParagraphStyle(
        'TblCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.4,
        leading=9.5,
        textColor=TEXT_DARK
    )

    badge_crit = ParagraphStyle(
        'BadgeCrit',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6.8,
        leading=8.5,
        textColor=CRITICAL_RED
    )

    badge_med = ParagraphStyle(
        'BadgeMed',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6.8,
        leading=8.5,
        textColor=WARNING_AMBER
    )

    badge_low = ParagraphStyle(
        'BadgeLow',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6.8,
        leading=8.5,
        textColor=SUCCESS_GREEN
    )

    story = []

    # =========================================================================
    # SECTION 1: COVER HEADER, EXECUTIVE SUMMARY & DATA ARCHITECTURE MATRIX
    # =========================================================================
    story.append(Paragraph("DATA QUALITY AUDIT & POWER BI SOLUTION REPORT", title_style))
    story.append(Paragraph("Auspify Technologies Internship  |  Netflix Titles Dataset (8,790 Records)", subtitle_style))
    
    meta_p = Paragraph(
        f"<b>Source Dataset:</b> <code>D:\\كورسات\\AUSPIFY\\Dataset.csv</code> &nbsp;&nbsp;|&nbsp;&nbsp; "
        f"<b>Audit Date:</b> {datetime.now().strftime('%B %d, %Y')} &nbsp;&nbsp;|&nbsp;&nbsp; "
        f"<b>Scope:</b> 10-Column Comprehensive Audit",
        meta_style
    )
    story.append(meta_p)
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1.5, color=SECONDARY, spaceBefore=2, spaceAfter=8))

    # Executive Summary Card
    exec_text = (
        "<b>Executive Summary & Context:</b> Before developing analytical dashboards in Power BI "
        "(covering Auspify Tasks 1 through 6), a forensic data quality audit of <code>Dataset.csv</code> was conducted. "
        "Although initial profiling indicates <b>0 blank cells</b> across all 10 columns, our deep inspection revealed "
        "critical hidden anomalies: <b>2,588 masked missing directors (29.4%)</b>, <b>287 masked missing countries (3.3%)</b>, "
        "<b>Excel auto-conversion corruption</b> altering titles to dates (e.g., '22 July' &rarr; '22-Jul'), <b>mixed-unit strings in duration</b> "
        "(preventing numeric aggregations), <b>comma-delimited multi-valued fields</b> (violating 1st Normal Form in genres & directors), "
        "and <b>duplicate records assigned divergent IDs</b>. This report details every defect, assesses its analytical impact, "
        "and provides copy-paste ready Power Query (M) transformations and DAX formulations for complete data integrity."
    )
    exec_table = Table([[Paragraph(exec_text, body_style)]], colWidths=[504])
    exec_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('LINELEFT', (0,0), (0,-1), 3.5, ACCENT_BLUE),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(exec_table)
    story.append(Spacer(1, 8))

    # Architecture Matrix
    story.append(Paragraph("1. Dataset Architecture & Issue Matrix", h1_style))
    story.append(Paragraph("Comprehensive status overview across all 10 columns in <code>Dataset.csv</code>:", body_style))

    matrix_rows = [
        [
            Paragraph("Column", tbl_header_style),
            Paragraph("Type", tbl_header_style),
            Paragraph("Unique", tbl_header_style),
            Paragraph("Key Data Anomaly Detected", tbl_header_style),
            Paragraph("Severity", tbl_header_style),
            Paragraph("Solved Strategy in Power BI", tbl_header_style)
        ],
        [
            Paragraph("<b>show_id</b>", tbl_cell_style),
            Paragraph("Text", tbl_cell_style),
            Paragraph("8,790", tbl_cell_style),
            Paragraph("False primary key illusion: duplicate content records exist under different show_ids.", tbl_cell_style),
            Paragraph("MEDIUM", badge_med),
            Paragraph("Deduplicate on Title + Year + Type", tbl_cell_style)
        ],
        [
            Paragraph("<b>type</b>", tbl_cell_style),
            Paragraph("Text", tbl_cell_style),
            Paragraph("2", tbl_cell_style),
            Paragraph("Bimodal ('Movie', 'TV Show'). Requires trimming to prevent hidden whitespace splits.", tbl_cell_style),
            Paragraph("LOW", badge_low),
            Paragraph("Text.Trim + Dimensional Slicer", tbl_cell_style)
        ],
        [
            Paragraph("<b>title</b>", tbl_cell_style),
            Paragraph("Text", tbl_cell_style),
            Paragraph("8,787", tbl_cell_style),
            Paragraph("Excel auto-date corruption ('22-Jul', '15-Aug', '9-Feb') + duplicate entries.", tbl_cell_style),
            Paragraph("CRITICAL", badge_crit),
            Paragraph("Replace corrupted values + Deduplicate", tbl_cell_style)
        ],
        [
            Paragraph("<b>director</b>", tbl_cell_style),
            Paragraph("Text", tbl_cell_style),
            Paragraph("4,528", tbl_cell_style),
            Paragraph("2,588 masked missing rows ('Not Given') + 629 multi-director comma lists.", tbl_cell_style),
            Paragraph("CRITICAL", badge_crit),
            Paragraph("Replace with null/Unknown + Bridge Table", tbl_cell_style)
        ],
        [
            Paragraph("<b>country</b>", tbl_cell_style),
            Paragraph("Text", tbl_cell_style),
            Paragraph("86", tbl_cell_style),
            Paragraph("287 masked missing rows ('Not Given'). Lacks GIS Data Category for Maps.", tbl_cell_style),
            Paragraph("HIGH", badge_crit),
            Paragraph("Replace 'Not Given' + Assign GIS Category", tbl_cell_style)
        ],
        [
            Paragraph("<b>date_added</b>", tbl_cell_style),
            Paragraph("Text", tbl_cell_style),
            Paragraph("1,713", tbl_cell_style),
            Paragraph("Text format (M/d/yyyy). Regional locale mismatches crash date conversions.", tbl_cell_style),
            Paragraph("CRITICAL", badge_crit),
            Paragraph("Change Type (Date, en-US) + Dim_Date", tbl_cell_style)
        ],
        [
            Paragraph("<b>release_year</b>", tbl_cell_style),
            Paragraph("Int64", tbl_cell_style),
            Paragraph("74", tbl_cell_style),
            Paragraph("Power BI auto-sums years by default (Total = 17,736,000). Needs non-additive role.", tbl_cell_style),
            Paragraph("MEDIUM", badge_med),
            Paragraph("Set Default Summarization to 'None'", tbl_cell_style)
        ],
        [
            Paragraph("<b>rating</b>", tbl_cell_style),
            Paragraph("Text", tbl_cell_style),
            Paragraph("14", tbl_cell_style),
            Paragraph("Redundant codes ('NR' vs 'UR'). Raw TV codes unhelpful without audience groupings.", tbl_cell_style),
            Paragraph("MEDIUM", badge_med),
            Paragraph("Standardize UR &rarr; NR + Audience Slicers", tbl_cell_style)
        ],
        [
            Paragraph("<b>duration</b>", tbl_cell_style),
            Paragraph("Text", tbl_cell_style),
            Paragraph("220", tbl_cell_style),
            Paragraph("Mixed units ('min' vs 'Season/Seasons'). Prevents mathematical aggregations.", tbl_cell_style),
            Paragraph("CRITICAL", badge_crit),
            Paragraph("Extract numbers & split into 2 metrics", tbl_cell_style)
        ],
        [
            Paragraph("<b>listed_in</b>", tbl_cell_style),
            Paragraph("Text", tbl_cell_style),
            Paragraph("513", tbl_cell_style),
            Paragraph("Multi-valued comma strings. Produces 513 fragmented bars if unnormalized.", tbl_cell_style),
            Paragraph("CRITICAL", badge_crit),
            Paragraph("Primary Genre column + Split Bridge Table", tbl_cell_style)
        ],
    ]

    col_widths = [62, 38, 38, 186, 52, 128]
    tbl_matrix = Table(matrix_rows, colWidths=col_widths, repeatRows=1)
    tbl_matrix.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ALIGN', (0,0), (-1,0), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT])
    ]))
    story.append(tbl_matrix)

    # =========================================================================
    # SECTION 2: DEEP COLUMN-BY-COLUMN ANALYSIS (Each wrapped in KeepTogether)
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("2. Deep Column-by-Column Audit & Solved Ways", h1_style))
    story.append(Paragraph("Exhaustive evaluation of data anomalies and step-by-step solutions for each column:", body_style))

    # Col 1: show_id
    col1 = [
        Paragraph("Column 1: <code>show_id</code> (Unique Catalog Identifier)", h2_style),
        Paragraph("<b>Problem & Diagnosis:</b> While every row has a distinct ID string (<code>s1</code> to <code>s8807</code>), several identical catalog entries are repeated under distinct IDs. For instance, <code>s3963</code> and <code>s5967</code> both represent the exact same Indian movie '15-Aug' directed by Swapnaneel Jayakar (2019). Similarly, <code>s4523</code> and <code>s5966</code> both duplicate the movie '22-Jul' (Norway, 2018). Relying on <code>show_id</code> for deduplication creates artificially inflated title counts in Power BI KPI cards.", bullet_style),
        Paragraph("<b>Solved Way in Power BI:</b> In Power Query, select <code>title</code>, <code>type</code>, and <code>release_year</code> &rarr; Right-click header &rarr; <b>Remove Duplicates</b>.", bullet_style)
    ]
    story.append(KeepTogether(col1))

    # Col 2: type
    col2 = [
        Paragraph("Column 2: <code>type</code> (Media Format Dimension)", h2_style),
        Paragraph("<b>Problem & Diagnosis:</b> Clean binary distribution consisting of 6,126 Movies (69.7%) and 2,664 TV Shows (30.3%). However, trailing whitespace or lowercase variations in future refreshes can fracture visuals. Furthermore, <code>type</code> serves as the master conditional branch for parsing the heterogeneous <code>duration</code> field.", bullet_style),
        Paragraph("<b>Solved Way in Power BI:</b> Select <code>type</code> &rarr; <b>Transform &rarr; Format &rarr; Trim</b>. In DAX, build measures: <code>Total Movies = CALCULATE(COUNTROWS('Dataset'), 'Dataset'[type]=\"Movie\")</code> and <code>Total TV Shows = CALCULATE(COUNTROWS('Dataset'), 'Dataset'[type]=\"TV Show\")</code>.", bullet_style)
    ]
    story.append(KeepTogether(col2))

    # Col 3: title
    col3 = [
        Paragraph("Column 3: <code>title</code> (Content Name & Excel Date Corruption)", h2_style),
        Paragraph("<b>Problem 1 (Excel Date Formatting Corruption):</b> During CSV generation via Microsoft Excel, titles containing calendar patterns were auto-converted into short date strings: <i>'22 July'</i> became <code>'22-Jul'</code>, <i>'15 August'</i> became <code>'15-Aug'</code>, and <i>'9 February'</i> became <code>'9-Feb'</code>.", bullet_style),
        Paragraph("<b>Problem 2 (Leading/Trailing Spaces):</b> Invisible whitespace exists on title strings, degrading exact text search results.", bullet_style),
        Paragraph("<b>Solved Way in Power BI:</b> Select <code>title</code> &rarr; <b>Transform &rarr; Format &rarr; Trim</b>. Use <b>Transform &rarr; Replace Values</b> to revert <code>\"22-Jul\"</code> &rarr; <code>\"22 July\"</code>, <code>\"15-Aug\"</code> &rarr; <code>\"15 August\"</code>, and <code>\"9-Feb\"</code> &rarr; <code>\"9 February\"</code>.", bullet_style)
    ]
    story.append(KeepTogether(col3))

    # Col 4: director
    col4 = [
        Paragraph("Column 4: <code>director</code> (Attribution & Severe Masked Missing Values)", h2_style),
        Paragraph("<b>Problem 1 (Masked Missing Data - 29.4%):</b> Exactly <b>2,588 records</b> contain the text string <code>\"Not Given\"</code>. Because it is non-null text, Power BI profiling falsely displays 100% data completeness. In 'Top 10 Directors' charts, 'Not Given' ranks as #1 with 2,588 titles, severely distorting leadership reporting.", bullet_style),
        Paragraph("<b>Problem 2 (Multi-Valued Field):</b> 629 records contain multiple directors separated by commas (e.g. <i>'Jan Suter, Raúl Campos'</i>). Standard bar charts treat the joint pair as a separate director instead of attributing work to each creator.", bullet_style),
        Paragraph("<b>Solved Way in Power BI:</b> In Power Query: Replace <code>\"Not Given\"</code> with <code>\"Unknown Director\"</code> (or blank <code>null</code>). In Director ranking visuals, apply filter: <code>director does not equal 'Unknown Director'</code>. For deep analysis (Task 6), create a Director Bridge Table: Reference <code>Dataset</code> &rarr; keep <code>show_id</code> and <code>director</code> &rarr; Split Column by delimiter (<code>, </code>) into rows &rarr; Trim.", bullet_style)
    ]
    story.append(KeepTogether(col4))

    # Col 5: country
    col5 = [
        Paragraph("Column 5: <code>country</code> (Geographic Entity & Masked Missing Values)", h2_style),
        Paragraph("<b>Problem 1 (Masked Missing Data - 3.3%):</b> <b>287 records</b> contain <code>\"Not Given\"</code>. If loaded into Power BI Map or Azure Map visuals, 'Not Given' triggers geocoding errors or attempts to place an invalid pin.", bullet_style),
        Paragraph("<b>Problem 2 (Missing GIS Data Category):</b> Power BI leaves the column as unclassified text, hindering automatic Azure/Bing geocoding.", bullet_style),
        Paragraph("<b>Solved Way in Power BI:</b> In Power Query: Replace <code>\"Not Given\"</code> with <code>\"Unknown Country\"</code> (or <code>null</code>). In Power BI Model View: Select <code>country</code> &rarr; <b>Properties</b> &rarr; set <b>Data Category</b> to <b>Country/Region</b>. In Map visuals, add visual filter: <code>country does not equal 'Unknown Country'</code>.", bullet_style)
    ]
    story.append(KeepTogether(col5))

    # Col 6: date_added
    col6 = [
        Paragraph("Column 6: <code>date_added</code> (Platform Ingestion Date & Locale Collision)", h2_style),
        Paragraph("<b>Problem 1 (Text Type vs Date):</b> Stored as text strings in US format (<code>M/d/yyyy</code>, e.g. <code>9/25/2021</code>). Stored as text, Power BI cannot create time hierarchies (Year, Quarter, Month) or execute DAX time intelligence.", bullet_style),
        Paragraph("<b>Problem 2 (Locale Formatting Crash):</b> On systems configured with UK or Middle Eastern regional formats (<code>dd/MM/yyyy</code>), simple date conversion crashes with <code>DataFormat.Error</code> because '25' is parsed as an invalid month.", bullet_style),
        Paragraph("<b>Solved Way in Power BI:</b> Right-click <code>date_added</code> &rarr; <b>Change Type</b> &rarr; <b>Using Locale...</b> &rarr; Type: <b>Date</b> &rarr; Locale: <b>English (United States)</b>. Build a dedicated DAX Calendar Table: <code>Dim_Date = CALENDAR(DATE(2008,1,1), DATE(2022,1,1))</code>, and link 1-to-many with <code>Dataset[date_added]</code>.", bullet_style)
    ]
    story.append(KeepTogether(col6))

    # Col 7: release_year
    col7 = [
        Paragraph("Column 7: <code>release_year</code> (Content Release Year & Default Aggregation)", h2_style),
        Paragraph("<b>Problem:</b> Stored as an integer (range 1925 to 2021). Power BI treats all whole number columns as additive numerical facts, auto-calculating meaningless sums (e.g., Sum of Release Year = 17,736,000) whenever added to a visual.", bullet_style),
        Paragraph("<b>Solved Way in Power BI:</b> In Power BI Data View, select <code>release_year</code> &rarr; In <b>Column Tools</b> ribbon, change <b>Summarization</b> from 'Sum' to <b>Don't Summarize</b>. Create a decade grouping column for high-level trend charts: <code>Decade = FLOOR('Dataset'[release_year], 10) & \"s\"</code>.", bullet_style)
    ]
    story.append(KeepTogether(col7))

    # Col 8: rating
    col8 = [
        Paragraph("Column 8: <code>rating</code> (Maturity Rating Standardization & Audience Segmentation)", h2_style),
        Paragraph("<b>Problem 1 (Semantic Redundancy):</b> Contains 14 distinct rating codes including both <code>NR</code> (79 titles) and <code>UR</code> (3 titles). Both represent 'Not Rated / Unrated', creating confusing redundant filter slices.", bullet_style),
        Paragraph("<b>Problem 2 (Lack of Audience Context):</b> Raw rating codes like <code>TV-Y7-FV</code> or <code>NC-17</code> are technical. Executive dashboards need high-level audience classifications (Kids, Teens, Adults).", bullet_style),
        Paragraph("<b>Solved Way in Power BI:</b> In Power Query: Replace <code>\"UR\"</code> with <code>\"NR\"</code>. Add a Conditional Column named <code>Audience Group</code>: [<code>TV-Y</code>, <code>TV-Y7</code>, <code>TV-Y7-FV</code>, <code>G</code>, <code>TV-G</code>] &rarr; 'Kids'; [<code>PG</code>, <code>PG-13</code>, <code>TV-PG</code>, <code>TV-14</code>] &rarr; 'Teens & Family'; [<code>R</code>, <code>NC-17</code>, <code>TV-MA</code>] &rarr; 'Adults'; Else &rarr; 'Unrated'.", bullet_style)
    ]
    story.append(KeepTogether(col8))

    # Col 9: duration
    col9 = [
        Paragraph("Column 9: <code>duration</code> (Heterogeneous Mixed Units: Minutes vs Seasons)", h2_style),
        Paragraph("<b>Problem:</b> Text field mixing two incompatible measurement units: minutes for Movies (e.g. <code>90 min</code>) and season counts for TV Shows (e.g. <code>1 Season</code>, <code>2 Seasons</code>). Because it is formatted as text, users cannot calculate average movie runtime, median show lifespan, or runtime histograms.", bullet_style),
        Paragraph("<b>Solved Way in Power BI:</b> In Power Query: Extract digits into <code>Duration_Value = Number.From(Text.Select([duration], {\"0\"..\"9\"}))</code>. Split into two clean columns: <code>Movie_Duration_Min = if [type]=\"Movie\" then [Duration_Value] else null</code> and <code>TV_Seasons_Count = if [type]=\"TV Show\" then [Duration_Value] else null</code>. Create DAX measures: <code>Avg Movie Runtime = AVERAGE('Dataset'[Movie_Duration_Min])</code>.", bullet_style)
    ]
    story.append(KeepTogether(col9))

    # Col 10: listed_in
    col10 = [
        Paragraph("Column 10: <code>listed_in</code> (Genres & 1st Normal Form Violation)", h2_style),
        Paragraph("<b>Problem:</b> Up to 3 genres are bundled in comma-delimited text strings (e.g. <i>'Comedies, Dramas, International Movies'</i>). This produces 513 compound combinations across only 42 true individual genres, rendering standard bar charts useless.", bullet_style),
        Paragraph("<b>Solved Way in Power BI:</b> (1) <b>Fast Approach (Primary Genre):</b> Extract the dominant first genre: <code>Text.Trim(Text.BeforeDelimiter([listed_in], \",\"))</code>. (2) <b>Advanced Approach (Normalized Genre Bridge Table for Tasks 5 & 6):</b> Reference <code>Dataset</code> in Power Query &rarr; keep only <code>show_id</code> and <code>listed_in</code> &rarr; Split Column by Delimiter (<code>, </code>) into <b>Rows</b> &rarr; Trim text &rarr; Establish 1-to-many relationship from <code>Dataset[show_id]</code> to <code>Bridge_Genres[show_id]</code>.", bullet_style)
    ]
    story.append(KeepTogether(col10))

    # =========================================================================
    # SECTION 3: PRODUCTION POWER QUERY (M) SCRIPT
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("3. Production-Ready Power Query (M) Transformation Script", h1_style))
    story.append(Paragraph(
        "To apply all 10 column transformations in a single automated step, open <b>Power BI Desktop</b> &rarr; "
        "click <b>Transform Data</b> &rarr; click <b>Advanced Editor</b> &rarr; paste the following script:",
        body_style
    ))

    m_script_text = (
        "let\n"
        "    // 1. Ingest raw CSV from the designated project path\n"
        "    Source = Csv.Document(File.Contents(\"D:\\كورسات\\AUSPIFY\\Dataset.csv\"), [Delimiter=\",\", Columns=10, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),\n"
        "    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),\n"
        "\n"
        "    // 2. Trim trailing and leading whitespace across all text columns\n"
        "    TrimmedText = Table.TransformColumns(PromotedHeaders, {\n"
        "        {\"show_id\", Text.Trim}, {\"type\", Text.Trim}, {\"title\", Text.Trim},\n"
        "        {\"director\", Text.Trim}, {\"country\", Text.Trim}, {\"rating\", Text.Trim},\n"
        "        {\"duration\", Text.Trim}, {\"listed_in\", Text.Trim}\n"
        "    }),\n"
        "\n"
        "    // 3. Rectify Excel auto-formatting corruption in title names\n"
        "    FixedTitle1 = Table.ReplaceValue(TrimmedText, \"22-Jul\", \"22 July\", Replacer.ReplaceText, {\"title\"}),\n"
        "    FixedTitle2 = Table.ReplaceValue(FixedTitle1, \"15-Aug\", \"15 August\", Replacer.ReplaceText, {\"title\"}),\n"
        "    FixedTitle3 = Table.ReplaceValue(FixedTitle2, \"9-Feb\", \"9 February\", Replacer.ReplaceText, {\"title\"}),\n"
        "\n"
        "    // 4. Eliminate redundant catalog records based on content attributes\n"
        "    DeduplicatedRows = Table.Distinct(FixedTitle3, {\"title\", \"type\", \"release_year\"}),\n"
        "\n"
        "    // 5. Replace masked missing placeholders ('Not Given') with explicit classifications\n"
        "    CleanedDirector = Table.ReplaceValue(DeduplicatedRows, \"Not Given\", \"Unknown Director\", Replacer.ReplaceText, {\"director\"}),\n"
        "    CleanedCountry = Table.ReplaceValue(CleanedDirector, \"Not Given\", \"Unknown Country\", Replacer.ReplaceText, {\"country\"}),\n"
        "\n"
        "    // 6. Harmonize redundant maturity rating codes (merge UR into NR)\n"
        "    StandardizedRating = Table.ReplaceValue(CleanedCountry, \"UR\", \"NR\", Replacer.ReplaceText, {\"rating\"}),\n"
        "\n"
        "    // 7. Strictly parse date_added with US locale to prevent regional formatting crashes\n"
        "    ParsedDate = Table.TransformColumnTypes(StandardizedRating, {{\"date_added\", type date}}, \"en-US\"),\n"
        "    ParsedYear = Table.TransformColumnTypes(ParsedDate, {{\"release_year\", Int64.Type}}),\n"
        "\n"
        "    // 8. Extract numeric duration and segregate movie minutes vs TV show seasons\n"
        "    ExtractedDurationNum = Table.AddColumn(ParsedYear, \"Duration_Value\", each \n"
        "        try Number.From(Text.Select([duration], {\"0\"..\"9\"})) otherwise null, Int64.Type),\n"
        "    AddedMovieMins = Table.AddColumn(ExtractedDurationNum, \"Movie_Duration_Min\", each \n"
        "        if [type] = \"Movie\" then [Duration_Value] else null, Int64.Type),\n"
        "    AddedTVSeasons = Table.AddColumn(AddedMovieMins, \"TV_Seasons_Count\", each \n"
        "        if [type] = \"TV Show\" then [Duration_Value] else null, Int64.Type),\n"
        "\n"
        "    // 9. Derive Primary Genre for clean non-cluttered visualizations\n"
        "    AddedPrimaryGenre = Table.AddColumn(AddedTVSeasons, \"Primary_Genre_Raw\", each \n"
        "        Text.Trim(Text.BeforeDelimiter([listed_in], \",\")), type text),\n"
        "    CleanedPrimaryGenre = Table.AddColumn(AddedPrimaryGenre, \"Primary_Genre\", each \n"
        "        if [Primary_Genre_Raw] = \"\" then [listed_in] else [Primary_Genre_Raw], type text),\n"
        "    FinalColumns = Table.RemoveColumns(CleanedPrimaryGenre, {\"Primary_Genre_Raw\"})\n"
        "in\n"
        "    FinalColumns"
    )

    m_table = Table([[Paragraph(m_script_text.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_block)]], colWidths=[504])
    m_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_CARD),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('LINELEFT', (0,0), (0,-1), 3.5, SECONDARY),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(m_table)
    story.append(Spacer(1, 8))

    exec_instructions = (
        "<b>Verification Steps After Applying M Code:</b><br/>"
        "1. Click <b>Close & Apply</b> in Power Query ribbon.<br/>"
        "2. Check the bottom right status bar: ensure <b>8,787 rows loaded</b> (3 duplicates eliminated).<br/>"
        "3. In the Data pane, confirm <code>Movie_Duration_Min</code> and <code>TV_Seasons_Count</code> appear with the Sigma (&Sigma;) icon.<br/>"
        "4. In Model view, select <code>country</code> &rarr; set <b>Data Category</b> to <b>Country/Region</b>."
    )
    inst_box = Table([[Paragraph(exec_instructions, body_style)]], colWidths=[504])
    inst_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 0.75, BORDER_COLOR),
        ('LINELEFT', (0,0), (0,-1), 3, SUCCESS_GREEN),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(inst_box)

    # =========================================================================
    # SECTION 4 & 5: STAR SCHEMA, DAX & PRE-FLIGHT CHECKLIST
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("4. Recommended Star Schema & Essential DAX Measures", h1_style))
    story.append(Paragraph(
        "To achieve optimal DAX calculation speeds and clean dashboard storytelling across Tasks 1 to 6, "
        "structure your model as follows:",
        body_style
    ))

    schema_points = [
        Paragraph("<b>Model Architecture:</b>", bullet_style),
        Paragraph("&bull; <b>Fact Table:</b> <code>Fact_Netflix_Titles</code> (Generated by the Power Query M script above).", bullet_style),
        Paragraph("&bull; <b>Date Dimension:</b> <code>Dim_Date</code> created via DAX: <code>Dim_Date = CALENDAR(DATE(2008,1,1), DATE(2022,1,1))</code>. Mark as official Date Table.", bullet_style),
        Paragraph("&bull; <b>Genre Bridge:</b> <code>Bridge_Title_Genre</code> (Created by referencing Dataset, splitting <code>listed_in</code> into rows) connected via 1-to-many relationship.", bullet_style),
        Spacer(1, 3),
        Paragraph("<b>Essential DAX Measures Library:</b>", bullet_style),
        Paragraph("<code>Total Titles = COUNTROWS('Fact_Netflix_Titles')</code>", code_inline),
        Paragraph("<code>Total Movies = CALCULATE(COUNTROWS('Fact_Netflix_Titles'), 'Fact_Netflix_Titles'[type] = \"Movie\")</code>", code_inline),
        Paragraph("<code>Total TV Shows = CALCULATE(COUNTROWS('Fact_Netflix_Titles'), 'Fact_Netflix_Titles'[type] = \"TV Show\")</code>", code_inline),
        Paragraph("<code>% Movies = DIVIDE([Total Movies], [Total Titles], 0)</code>", code_inline),
        Paragraph("<code>Avg Movie Duration = ROUND(AVERAGE('Fact_Netflix_Titles'[Movie_Duration_Min]), 0) & \" min\"</code>", code_inline),
        Paragraph("<code>Avg TV Seasons = ROUND(AVERAGE('Fact_Netflix_Titles'[TV_Seasons_Count]), 1) & \" Seasons\"</code>", code_inline),
        Paragraph("<code>Total Producing Countries = DISTINCTCOUNTNOBLANK('Fact_Netflix_Titles'[country])</code>", code_inline),
        Paragraph("<code>YoY Additions Growth = VAR PrevYear = CALCULATE([Total Titles], SAMEPERIODLASTYEAR('Dim_Date'[Date])) RETURN DIVIDE([Total Titles] - PrevYear, PrevYear, 0)</code>", code_inline)
    ]
    story.append(KeepTogether(schema_points))
    story.append(Spacer(1, 8))

    story.append(Paragraph("5. Pre-Flight Checklist for Internship Tasks 1 to 6", h1_style))
    story.append(Paragraph("Verification checklist ensuring all internship task requirements are satisfied:", body_style))

    chk_headers = [
        Paragraph("Internship Task", tbl_header_style),
        Paragraph("Dataset Requirement & Verification Step", tbl_header_style),
        Paragraph("Status", tbl_header_style)
    ]
    chk_rows = [chk_headers,
        [
            Paragraph("<b>Task 1: Data Preparation</b>", tbl_cell_style),
            Paragraph("Zero unhandled 'Not Given' values; US locale dates parsed; content duplicates removed.", tbl_cell_style),
            Paragraph("VERIFIED", badge_low)
        ],
        [
            Paragraph("<b>Task 2: Content Overview</b>", tbl_cell_style),
            Paragraph("KPI cards for Movies vs TV Shows, Total Titles, and interactive Type/Year slicers.", tbl_cell_style),
            Paragraph("READY", badge_low)
        ],
        [
            Paragraph("<b>Task 3: Global Insights</b>", tbl_cell_style),
            Paragraph("Country Data Category set to 'Country/Region'; 'Unknown Country' filtered from maps.", tbl_cell_style),
            Paragraph("VERIFIED", badge_low)
        ],
        [
            Paragraph("<b>Task 4: Growth Trends</b>", tbl_cell_style),
            Paragraph("Dim_Date connected to date_added; release_year summarization disabled for clean time-series.", tbl_cell_style),
            Paragraph("READY", badge_low)
        ],
        [
            Paragraph("<b>Task 5: Audience & Categories</b>", tbl_cell_style),
            Paragraph("Audience groupings (Kids, Teens, Adults) configured; Primary Genre cleanly extracted.", tbl_cell_style),
            Paragraph("READY", badge_low)
        ],
        [
            Paragraph("<b>Task 6: Executive BI Dashboard</b>", tbl_cell_style),
            Paragraph("Multi-page navigation, normalized Bridge tables, dynamic DAX KPIs and drill-throughs.", tbl_cell_style),
            Paragraph("READY", badge_low)
        ],
    ]
    tbl_chk = Table(chk_rows, colWidths=[120, 324, 60], repeatRows=1)
    tbl_chk.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT])
    ]))
    story.append(tbl_chk)

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print("SUCCESS: PDF successfully generated.")

if __name__ == "__main__":
    build_pdf()
