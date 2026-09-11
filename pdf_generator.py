from pathlib import Path
from html import escape

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle,
)
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable,
    PageBreak,
)

from schemas import ModulePlan


OUTPUT_DIR = Path("generated_modules")


def generate_module_pdf(
    module: ModulePlan,
    topic: str
) -> Path:

    OUTPUT_DIR.mkdir(exist_ok=True)

    output_path = OUTPUT_DIR / f"{module.code}.pdf"

    document = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
        title=f"{module.code} - {module.title}",
        author="SkillFoundry",
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ModuleTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=26,
        alignment=TA_CENTER,
        spaceAfter=8,
    )

    code_style = ParagraphStyle(
        "ModuleCode",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        alignment=TA_CENTER,
        spaceAfter=6,
    )

    topic_style = ParagraphStyle(
        "Topic",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        alignment=TA_CENTER,
        spaceAfter=18,
    )

    section_style = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        spaceBefore=12,
        spaceAfter=8,
    )

    exercise_style = ParagraphStyle(
        "Exercise",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        spaceBefore=12,
        spaceAfter=6,
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=15,
        spaceAfter=6,
    )

    evidence_style = ParagraphStyle(
        "Evidence",
        parent=body_style,
        leftIndent=10,
        spaceBefore=4,
        spaceAfter=10,
    )

    story = []

    # Header
    story.append(
        Paragraph(
            escape(module.code),
            code_style,
        )
    )

    story.append(
        Paragraph(
            escape(module.title),
            title_style,
        )
    )

    story.append(
        Paragraph(
            f"SkillFoundry - {escape(topic)}",
            topic_style,
        )
    )

    story.append(
        HRFlowable(
            width="100%",
            thickness=1,
            spaceAfter=15,
        )
    )

    # Prerequisites
    story.append(
        Paragraph(
            "Prerequisites",
            section_style,
        )
    )

    if module.prerequisites:
        for prerequisite in module.prerequisites:
            story.append(
                Paragraph(
                    f"- {escape(prerequisite)}",
                    body_style,
                )
            )
    else:
        story.append(
            Paragraph(
                "No prerequisites.",
                body_style,
            )
        )

    # Objectives
    story.append(
        Paragraph(
            "Learning Objectives",
            section_style,
        )
    )

    for objective in module.objectives:
        story.append(
            Paragraph(
                f"- {escape(objective)}",
                body_style,
            )
        )

    # Exercises
    story.append(
        Paragraph(
            "Exercises",
            section_style,
        )
    )

    for exercise in module.exercises:

        story.append(
            Paragraph(
                f"{escape(exercise.code)} - {escape(exercise.title)}",
                exercise_style,
            )
        )

        story.append(
            Paragraph(
                f"<b>Task:</b> {escape(exercise.task)}",
                body_style,
            )
        )

        story.append(
            Paragraph(
                f"<b>Evidence required:</b> "
                f"{escape(exercise.evidence_type)}",
                evidence_style,
            )
        )

    # Assessment
    story.append(
        Paragraph(
            "Assessment Methods",
            section_style,
        )
    )

    for method in module.assessment_methods:
        story.append(
            Paragraph(
                f"- {escape(method)}",
                body_style,
            )
        )

    # Mastery
    story.append(
        Paragraph(
            "Mastery Criteria",
            section_style,
        )
    )

    for criterion in module.mastery_criteria:
        story.append(
            Paragraph(
                f"- {escape(criterion)}",
                body_style,
            )
        )

    def add_footer(canvas, doc):
        canvas.saveState()

        canvas.setFont(
            "Helvetica",
            8,
        )

        canvas.drawString(
            20 * mm,
            10 * mm,
            f"SkillFoundry | {module.code}",
        )

        canvas.drawRightString(
            A4[0] - 20 * mm,
            10 * mm,
            f"Page {doc.page}",
        )

        canvas.restoreState()

    document.build(
        story,
        onFirstPage=add_footer,
        onLaterPages=add_footer,
    )

    return output_path