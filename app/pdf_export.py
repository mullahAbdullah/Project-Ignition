from io import BytesIO

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


def create_proposal_pdf(profile: dict, solution_text: str) -> bytes:
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("AI Automation Proposal", styles["Heading1"]))
    story.append(Spacer(1, 20))

    story.append(Paragraph("<b>Client</b>", styles["Heading2"]))
    story.append(
        Paragraph(
            f"Company: {profile.get('company') or 'Prospective Client'}",
            styles["BodyText"],
        )
    )

    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Contact</b>", styles["Heading2"]))
    story.append(
        Paragraph(
            f"Decision Maker: {profile.get('decision_maker') or 'To Be Confirmed'}",
            styles["BodyText"],
        )
    )

    story.append(
        Paragraph(
            f"Industry: {profile.get('industry') or 'General Business'}",
            styles["BodyText"],
        )
    )
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Business Need</b>", styles["Heading2"]))

    story.append(
        Paragraph(
            profile.get("goal") or "Business automation solution tailored to client requirements.",
            styles["BodyText"],
        )
    )
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Proposed Solution</b>", styles["Heading2"]))

    story.append(
        Paragraph(
            "We propose implementing a customized AI solution designed specifically for this business.",
            styles["BodyText"],
        )
    )

    story.append(Spacer(1, 8))

    story.append(
        Paragraph(
            solution_text.replace("\n", "<br/>"),
            styles["BodyText"],
        )
    )
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Estimated Project Scope</b>", styles["Heading2"]))

    story.append(
        Paragraph(
            f"Budget: {profile.get('budget') or 'To Be Discussed'}",
            styles["BodyText"],
        )
    )

    story.append(
        Paragraph(
            f"Timeline: {profile.get('timeline') or 'To Be Discussed'}",
            styles["BodyText"],
        )
    )
    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "Thank you for considering Project Ignition.",
            styles["Heading2"],
        )
    )

    story.append(
        Paragraph(
            "We look forward to helping your business automate customer interactions, improve efficiency, and deliver an outstanding customer experience.",
            styles["BodyText"],
        )
    )

    doc.build(story)

    pdf = buffer.getvalue()
    buffer.close()

    return pdf