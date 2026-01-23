"""Simple visualization module that generates static HTML files with Chart.js.

This follows the pattern from the Gemini CLI course - generate HTML files directly
and open them in the browser. No server required.
"""

import json
import os
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import uuid


# Output directory for generated charts (inside project folder)
CHARTS_DIR = Path(__file__).parent.parent / "charts"


def ensure_charts_dir() -> Path:
    """Ensure the charts directory exists."""
    CHARTS_DIR.mkdir(exist_ok=True)
    return CHARTS_DIR


def generate_chart_html(
    data: List[Dict[str, Any]],
    chart_type: str,
    x_column: str,
    y_column: str,
    title: str = "Data Visualization",
    open_browser: bool = False,
) -> Dict[str, Any]:
    """
    Generate a static HTML file with an embedded Chart.js visualization.
    
    Args:
        data: List of dictionaries containing the data
        chart_type: Type of chart (bar, line, pie, scatter, doughnut)
        x_column: Column name for labels/X-axis
        y_column: Column name for values/Y-axis
        title: Chart title
        open_browser: Whether to automatically open the chart in browser
    
    Returns:
        Dictionary with success status and file path
    """
    try:
        ensure_charts_dir()
        
        # Extract data
        labels = [str(row.get(x_column, "")) for row in data if x_column in row]
        values = [row.get(y_column, 0) for row in data if y_column in row]
        
        if not labels or not values:
            return {
                "success": False,
                "error": f"Columns '{x_column}' or '{y_column}' not found in data"
            }
        
        # Generate chart ID and filename
        chart_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chart_{timestamp}_{chart_id}.html"
        filepath = CHARTS_DIR / filename
        
        # Generate colors
        colors = generate_colors(len(labels))
        
        # Create HTML content
        html_content = create_chart_html(
            title=title,
            chart_type=chart_type,
            labels=labels,
            values=values,
            colors=colors,
            x_label=x_column,
            y_label=y_column,
        )
        
        # Write file
        filepath.write_text(html_content)
        
        # Open in browser if requested
        if open_browser:
            webbrowser.open(f"file://{filepath.absolute()}")
        
        return {
            "success": True,
            "chart_id": chart_id,
            "file_path": str(filepath.absolute()),
            "message": f"Chart saved to {filepath.name}" + (" and opened in browser" if open_browser else ""),
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def generate_colors(count: int) -> List[str]:
    """Generate a list of colors for the chart."""
    base_colors = [
        "rgba(54, 162, 235, 0.8)",   # Blue
        "rgba(255, 99, 132, 0.8)",   # Red
        "rgba(75, 192, 192, 0.8)",   # Teal
        "rgba(255, 206, 86, 0.8)",   # Yellow
        "rgba(153, 102, 255, 0.8)",  # Purple
        "rgba(255, 159, 64, 0.8)",   # Orange
        "rgba(46, 204, 113, 0.8)",   # Green
        "rgba(142, 68, 173, 0.8)",   # Violet
        "rgba(241, 196, 15, 0.8)",   # Gold
        "rgba(231, 76, 60, 0.8)",    # Coral
    ]
    # Cycle through colors if we need more than 10
    return [base_colors[i % len(base_colors)] for i in range(count)]


def create_chart_html(
    title: str,
    chart_type: str,
    labels: List[str],
    values: List[Any],
    colors: List[str],
    x_label: str,
    y_label: str,
) -> str:
    """Create the HTML content for the chart."""
    
    # Map chart types
    chart_type_map = {
        "bar": "bar",
        "line": "line",
        "pie": "pie",
        "doughnut": "doughnut",
        "scatter": "scatter",
    }
    js_chart_type = chart_type_map.get(chart_type.lower(), "bar")
    
    # Prepare data for JavaScript
    labels_json = json.dumps(labels)
    values_json = json.dumps(values)
    colors_json = json.dumps(colors)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #1a1a2e;
            color: #eee;
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}
        h1 {{
            text-align: center;
            margin-bottom: 20px;
            color: #00d4ff;
        }}
        .chart-container {{
            background: #16213e;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }}
        .meta {{
            margin-top: 20px;
            padding: 15px;
            background: #0f3460;
            border-radius: 8px;
            font-size: 0.9rem;
            color: #aaa;
        }}
        .meta span {{
            margin-right: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <div class="chart-container">
            <canvas id="chart"></canvas>
        </div>
        <div class="meta">
            <span><strong>Chart Type:</strong> {chart_type}</span>
            <span><strong>Data Points:</strong> {len(values)}</span>
            <span><strong>Generated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</span>
        </div>
    </div>
    
    <script>
        const ctx = document.getElementById('chart').getContext('2d');
        const labels = {labels_json};
        const values = {values_json};
        const colors = {colors_json};
        
        new Chart(ctx, {{
            type: '{js_chart_type}',
            data: {{
                labels: labels,
                datasets: [{{
                    label: '{y_label}',
                    data: values,
                    backgroundColor: colors,
                    borderColor: colors.map(c => c.replace('0.8', '1')),
                    borderWidth: 2,
                    tension: 0.3,
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        labels: {{ color: '#eee' }}
                    }},
                    title: {{
                        display: false
                    }}
                }},
                scales: {{
                    x: {{
                        ticks: {{ color: '#aaa' }},
                        grid: {{ color: 'rgba(255,255,255,0.1)' }},
                        title: {{
                            display: true,
                            text: '{x_label}',
                            color: '#aaa'
                        }}
                    }},
                    y: {{
                        ticks: {{ color: '#aaa' }},
                        grid: {{ color: 'rgba(255,255,255,0.1)' }},
                        title: {{
                            display: true,
                            text: '{y_label}',
                            color: '#aaa'
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>"""
    
    return html


# Convenience function for quick chart generation
def bar_chart(data: List[Dict], x: str, y: str, title: str = "Bar Chart") -> Dict[str, Any]:
    """Generate a bar chart."""
    return generate_chart_html(data, "bar", x, y, title)


def line_chart(data: List[Dict], x: str, y: str, title: str = "Line Chart") -> Dict[str, Any]:
    """Generate a line chart."""
    return generate_chart_html(data, "line", x, y, title)


def pie_chart(data: List[Dict], x: str, y: str, title: str = "Pie Chart") -> Dict[str, Any]:
    """Generate a pie chart."""
    return generate_chart_html(data, "pie", x, y, title)


if __name__ == "__main__":
    # Test the visualization
    test_data = [
        {"category": "Electronics", "sales": 1500},
        {"category": "Clothing", "sales": 1200},
        {"category": "Food", "sales": 800},
        {"category": "Books", "sales": 600},
        {"category": "Sports", "sales": 450},
    ]
    
    result = generate_chart_html(
        data=test_data,
        chart_type="bar",
        x_column="category",
        y_column="sales",
        title="Sales by Category",
    )
    print(result)
