from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from datetime import datetime


def create_pdf(user_name, prediction, risk_percentage, recommendation):

    filename = f"Mental_Health_Report_{user_name}.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    title_style = styles["Heading1"]
    title_style.alignment = TA_CENTER
    title_style.textColor = HexColor("#2563EB")

    heading_style = styles["Heading2"]
    heading_style.textColor = HexColor("#2563EB")

    normal = styles["BodyText"]

    story = []

    # -----------------------------
    # Title
    # -----------------------------

    story.append(
        Paragraph(
            "Student Mental Health Assessment Report",
            title_style
        )
    )

    story.append(Spacer(1, 0.3 * inch))

    # -----------------------------
    # Student Details
    # -----------------------------

    story.append(
        Paragraph(
            f"<b>Student Name:</b> {user_name}",
            normal
        )
    )

    story.append(
        Paragraph(
            f"<b>Date:</b> {datetime.now().strftime('%d %B %Y %I:%M %p')}",
            normal
        )
    )

    story.append(Spacer(1, 0.25 * inch))

    # -----------------------------
    # Prediction
    # -----------------------------

    story.append(
        Paragraph(
            "Assessment Result",
            heading_style
        )
    )

    risk = "High Mental Health Risk" if prediction == 1 else "Low Mental Health Risk"

    story.append(
        Paragraph(
            f"<b>Prediction:</b> {risk}",
            normal
        )
    )

    story.append(
        Paragraph(
            f"<b>Risk Score:</b> {risk_percentage}%",
            normal
        )
    )

    story.append(Spacer(1, 0.25 * inch))

    # -----------------------------
    # AI Recommendation
    # -----------------------------

    story.append(
        Paragraph(
            "AI Wellness Recommendations",
            heading_style
        )
    )

    recommendation = recommendation.replace("\n", "<br/>")

    story.append(
        Paragraph(
            recommendation,
            normal
        )
    )

    story.append(Spacer(1, 0.3 * inch))

    # -----------------------------
    # Disclaimer
    # -----------------------------

    story.append(
        Paragraph(
            "Disclaimer",
            heading_style
        )
    )

    story.append(
        Paragraph(
            "This report is generated using a Machine Learning model "
            "and AI-generated recommendations. It is intended for "
            "educational purposes only and should not be considered "
            "a medical diagnosis or professional mental health advice.",
            normal
        )
    )

    doc.build(story)

    return filename