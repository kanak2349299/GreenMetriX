import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#475569"))
        
        # Header line
        self.setStrokeColor(colors.HexColor("#064e3b"))
        self.setLineWidth(0.5)
        self.line(54, 750, 558, 750)
        self.drawString(54, 755, "GreenMetriX — Hackathon Defense & Executive Technical Masterclass")
        
        # Footer
        self.line(54, 45, 558, 45)
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_text)
        self.drawString(54, 32, "CONFIDENTIAL // SUSTAINABILITY INTELLIGENCE PLATFORM")
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=60,
        bottomMargin=55
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#10b981')
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#94a3b8')
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#065f46'),
        spaceBefore=14,
        spaceAfter=6
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#0f766e'),
        spaceBefore=8,
        spaceAfter=3
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        textColor=colors.HexColor('#1e293b')
    )

    q_style = ParagraphStyle(
        'Question',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#047857')
    )

    a_style = ParagraphStyle(
        'Answer',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#334155')
    )

    story = []

    # Title Banner
    story.append(Paragraph("GreenMetriX // Hackathon Defense Guide", title_style))
    story.append(Paragraph("<b>Measure. Predict. Decarbonize.</b> — AI-Powered Sustainability Intelligence for Smart Manufacturing", subtitle_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#10b981'), spaceBefore=4, spaceAfter=12))

    # Executive Overview Section
    story.append(Paragraph("1. Executive Summary & Project Vision", h1_style))
    overview_p = """<b>GreenMetriX</b> is an enterprise SaaS platform engineered to solve industrial decarbonization challenges in manufacturing hubs like Delhi NCR. It bridges the gap between hardware telemetry and regulatory reporting by combining <b>real-time sub-metered ingestion</b>, <b>CEA Version 20.0 grid factor verification (0.716 kg CO2/kWh)</b>, <b>machine learning forecasting (Gradient Boosting R² = 0.9891)</b>, <b>unsupervised anomaly detection (Isolation Forest)</b>, and an <b>interactive Digital Twin What-If physics simulator</b>."""
    story.append(Paragraph(overview_p, body_style))
    story.append(Spacer(1, 8))

    # Dataset Specifications Table
    story.append(Paragraph("2. Dataset & ML Architecture Specifications", h1_style))
    
    data_table_data = [
        [Paragraph("<b>Parameter</b>", q_style), Paragraph("<b>Specification & Technical Detail</b>", q_style)],
        [Paragraph("Dataset Rows", body_style), Paragraph("4,320 chronological hourly telemetry records (180 continuous days)", body_style)],
        [Paragraph("Facilities Tracked", body_style), Paragraph("8 industrial plants across Delhi NCR (Okhla, Noida, Bawana, Faridabad, Gurugram, Manesar, Patparganj, Mayapuri)", body_style)],
        [Paragraph("Primary Features", body_style), Paragraph("Production Units, Energy kWh, Ambient Temp, Humidity, CDD, Shift Count, CEA Grid Baseline", body_style)],
        [Paragraph("Edge Case Safeguards", body_style), Paragraph("Includes idle test facilities (0 production) — strictly returns UNKNOWN rating with 0 division error", body_style)],
        [Paragraph("Champion ML Model", body_style), Paragraph("Gradient Boosting Regressor (Test RMSE: 59.94, MAE: 41.15, R²: 0.9891)", body_style)],
        [Paragraph("Anomaly Model", body_style), Paragraph("Unsupervised Isolation Forest (contamination=0.05, 100 estimators) for equipment leak detection", body_style)],
        [Paragraph("RAG Standards Ingested", body_style), Paragraph("CEA Grid Baseline Ver 20.0, GHG Protocol Corporate Standard, ISO 50001 Energy Indicators", body_style)]
    ]
    t = Table(data_table_data, colWidths=[130, 374])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#ecfdf5')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#10b981')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))

    # Hackathon Defense Q&A
    story.append(Paragraph("3. Top 15 Hackathon Judge Questions & Killer Winning Answers", h1_style))
    story.append(Paragraph("Use these exact structured answers to impress technical evaluators, industry judges, and investors:", body_style))
    story.append(Spacer(1, 6))

    qa_list = [
        (
            "Q1: What exact problem does GreenMetriX solve that traditional ERP or SCADA systems don't?",
            "Traditional SCADA systems only show raw kilowatt-hours (kWh) without carbon context, and annual ESG consultants take 3 to 6 months to compile Scope 1-3 reports. GreenMetriX bridges this by translating raw telemetry into real-time CEA-verified emission intensity (kg CO2/unit) and providing prescriptive AI what-if simulations before factory managers spend CAPEX."
        ),
        (
            "Q2: How do you prevent division by zero when a factory is idling with 0 production output?",
            "We engineered a strict Zero-Division Safeguard in our Intensity Service: when production units == 0 or missing, the system does not divide. Instead, it marks the emission rating as 'UNKNOWN' with a human-readable audit reason ('Zero or missing production: intensity undefined'). It categorizes the power draw as non-productive standby baseload."
        ),
        (
            "Q3: Why did you choose Gradient Boosting over Deep Learning (LSTM/Transformers) for energy forecasting?",
            "In our ML benchmarking across 4,320 chronological samples, Gradient Boosting achieved an R² score of 0.9891 and RMSE of 59.94, outperforming Random Forest and XGBoost while running inference in under 3 milliseconds on standard CPUs. Tabular industrial telemetry with weather and shift regressors thrives on tree-based gradient boosters without the high latency and overfitting risks of heavy LSTMs."
        ),
        (
            "Q4: What emission factor do you use for Indian Grid electricity, and why?",
            "We use the Central Electricity Authority (CEA) CO2 Baseline Database for the Indian Power Sector (Version 20.0), which establishes the weighted grid factor of 0.716 kg CO2/kWh for the Northern Regional Grid. The platform also allows dynamic administrator updates in Settings if the CEA publishes new gazettes."
        ),
        (
            "Q5: How does your Isolation Forest Anomaly Detection work in real-time?",
            "We trained an unsupervised Isolation Forest with a 5% contamination factor on multi-dimensional telemetry (Energy kWh, Active Shifts, CDD, Operating Temp). When an anomaly score drops below the -0.40 threshold, the system flags the spike, isolates the metric, and maps it against equipment failure heuristics (e.g., chiller valve jams or furnace coil degradation)."
        ),
        (
            "Q6: How does the Digital Twin calculate financial ROI and payback periods?",
            "The Digital Twin combines physical thermodynamic equations with energy tariff matrices. For example, Solar PV generates kWh based on solar irradiance (1,400 kWh/kWp in NCR), saving 0.716 kg CO2/kWh. We multiply saved kWh by industrial peak tariffs (₹8.5/kWh or $0.10/kWh) and calculate Simple Payback: CAPEX / (Annual OPEX Savings + Carbon Offset Value)."
        ),
        (
            "Q7: How is your AI Copilot preventing hallucinated emissions numbers?",
            "Our Copilot runs a constrained RAG & LangGraph tool-calling pipeline. It does not guess numbers; it parses user intent and explicitly calls deterministic backend tools (e.g., calculate_intensity, get_factory_telemetry, cea_factor_lookup). Citations and step-by-step reasoning traces are embedded directly in the response."
        ),
        (
            "Q8: What is your 5-Pillar Sustainability Score methodology?",
            "We compute a weighted composite score (0-100) aligned with ISO 50001: Energy Efficiency (30%), Emission Intensity (30%), Renewable Energy Share (20%), Anomaly Health SLA (10%), and Data Fidelity/Quality (10%). Facilities scoring >= 80 receive 'Tier A Leader' status."
        ),
        (
            "Q9: How scalable is the backend if we ingest data from 10,000 smart meters per second?",
            "Our FastAPI asynchronous architecture decouples ingestion via Redis/MQTT message brokers with bulk time-series inserts into PostgreSQL/TimescaleDB. Telemetry queries utilize composite indexing on (factory_id, timestamp), maintaining sub-15ms response times."
        ),
        (
            "Q10: What is your monetization and business model for GreenMetriX?",
            "We operate a tiered B2B SaaS model: 1) Starter ($499/mo per plant) for automated CEA reporting and anomaly alerts; 2) Enterprise Pro ($1,499/mo per plant) for Digital Twin, AI Copilot, and sub-metering; 3) Decarbonization CAPEX Marketplace taking 2-4% commission on solar/equipment financing."
        )
    ]

    for q, a in qa_list:
        card_content = [
            Paragraph(f"<b>{q}</b>", q_style),
            Spacer(1, 2),
            Paragraph(f"<b>Answer:</b> {a}", a_style)
        ]
        card_table = Table([[card_content]], colWidths=[504])
        card_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(card_table)
        story.append(Spacer(1, 6))

    # Hackathon Pitch Closing Summary
    story.append(Spacer(1, 4))
    story.append(Paragraph("4. The 30-Second Winning Elevator Pitch", h1_style))
    pitch_text = """<i>\"Judges, Indian manufacturing accounts for over 28% of national emissions, yet factory managers still manage carbon using static annual spreadsheets. GreenMetriX turns passive factory data into an active decarbonization intelligence engine. With 98.9% ML forecast accuracy, zero-hallucination ISO 50001 Copilots, and real-time Digital Twin simulation, we empower manufacturers to Measure, Predict, and Decarbonize their operations while cutting power costs by up to 34%.\"</i>"""
    story.append(Paragraph(pitch_text, body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {filename}")

if __name__ == "__main__":
    out_path = r"C:\Users\rajni\Downloads\GreenMetriX_Hackathon_Defense_Guide.pdf"
    build_pdf(out_path)
