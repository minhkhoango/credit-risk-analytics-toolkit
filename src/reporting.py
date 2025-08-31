# src/reporting.py
"""
Handles the generation of the final PDF report.
"""
import base64
import io
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

import jinja2
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from weasyprint import HTML  # type: ignore[import]

if TYPE_CHECKING:
    from .engine import SimulationResults


def create_lift_chart(results: "SimulationResults") -> str:
    """
    Creates a chart visualizing the simulation lift
    and returns it as a base64 string.
    """
    total_apps: int = results["total_applications_processed"]
    approved_lift: int = results["decisions_flipped_to_approve"]
    remaining_declines = total_apps - approved_lift

    labels = ["Potential New Approvals", "Remaining Declines"]
    sizes = [approved_lift, remaining_declines]
    colors = ["#2a6ed4", "#c7d7f0"]  # Nova Credit blue tones

    fig: Figure
    ax: Axes
    fig, ax = plt.subplots()  # type: ignore[assignment]
    ax.bar(labels, sizes, color=colors)  # type: ignore[attr-defined]

    ax.set_ylabel("Number of Applications")  # type: ignore[attr-defined]
    ax.set_title(  # type: ignore[attr-defined,type-ignore]
        "Portfolio Lift Analysis", fontsize=14, fontweight="bold"
    )
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.grid(True, linestyle="--", alpha=0.6)  # type: ignore[attr-defined]
    ax.set_axisbelow(True)

    # Add data labels
    for i, v in enumerate(sizes):
        ax.text(  # type: ignore[attr-defined,type-ignore]
            i, v + (total_apps * 0.01), str(v), ha="center", fontweight="bold"
        )

    # Use a buffer to save the plot to memory instead of a file
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")  # type: ignore[attr-defined]
    plt.close(fig)
    buf.seek(0)

    # Encode the image in base64 to embed in the HTML
    img_str = base64.b64encode(buf.read()).decode("utf-8")
    return f"data:image/png;base64,{img_str}"


def generate_pdf_report(results: "SimulationResults", output_path: Path) -> None:
    """
    Generates a professional PDF report from simulation results.

    Args:
        results: The dictionary of results from the RetroSimulationEngine.
        output_path: The path to save the final PDF file.
    """
    template_dir = Path(__file__).parent.parent / "templates"
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
    template = env.get_template("report_template.html")

    # Generate the chart and add it to the results context
    chart_image_b64 = create_lift_chart(results)

    # Prepare data for the template
    current_date = datetime.now().strftime("%B %d, %Y")
    template_context: dict[str, Any] = {
        "results": results,
        "current_date": current_date,
        "chart_image": chart_image_b64,
    }

    # Render the HTML template
    html_out = template.render(template_context)

    # Generate the PDF
    # The base_url is crucial for WeasyPrint to find the CSS file
    HTML(string=html_out, base_url=str(template_dir)).write_pdf(  # type: ignore
        output_path
    )
