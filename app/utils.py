from typing import Dict, Any

def build_summary(scan_data: Dict[str, Any]) -> Dict[str, int]:
    """
    Construye un resumen con estadísticas clave del análisis de VirusTotal.
    """
    stats = scan_data["data"]["attributes"]["stats"]
    summary = {
        "Malicious": stats.get("malicious", 0),
        "Suspicious": stats.get("suspicious", 0),
        "Undetected": stats.get("undetected", 0),
        "Harmless": stats.get("harmless", 0),
        "Timeout": stats.get("timeout", 0),
        "Confirmed Timeout": stats.get("confirmed-timeout", 0),
        "Failure": stats.get("failure", 0),
        "Unsupported": stats.get("type-unsupported", 0),
    }
    
    return summary


def generate_html_from_analysis(analysis_result: Dict[str, Any], filename: str) -> str:
    """
    Genera una tabla HTML con los resultados del análisis de VirusTotal.
    """
    results = analysis_result.get("data", {}).get("attributes", {}).get("results", {})
    
    rows = ""
    for engine, info in results.items():
        rows += f"""
        <tr>
            <td>{engine}</td>
            <td>{info.get('engine_name')}</td>
            <td>{info.get('engine_version')}</td>
            <td>{info.get('engine_update')}</td>
            <td>{info.get('category')}</td>
            <td>{info.get('result') or '-'}</td>
        </tr>
        """

    html = f"""
    <html>
        <head>
            <title>Resultados del Análisis</title>
            <style>
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h1>Resultados del Análisis para archivo: {filename}</h1>
            <table>
                <thead>
                    <tr>
                        <th>Motor</th>
                        <th>Nombre</th>
                        <th>Versión</th>
                        <th>Actualización</th>
                        <th>Categoría</th>
                        <th>Resultado</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </body>
    </html>
    """
    
    return html

