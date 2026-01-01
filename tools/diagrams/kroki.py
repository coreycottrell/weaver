#!/usr/bin/env python3
"""
Kroki Diagram Generator

Generate diagrams from text-based descriptions (Mermaid, PlantUML, GraphViz, etc.)
using the free Kroki.io API. No authentication required.

Origin: A-C-Gee (AI-CIV Team 2)
Shared via: AI-CIV Comms Hub Skills Library

Usage:
    from tools.diagrams.kroki import generate_diagram

    # Generate a Mermaid flowchart
    code = '''
    flowchart TD
        A[Start] --> B[End]
    '''
    path = generate_diagram(code, "/tmp/flowchart.png")

Reference:
    - Kroki API: https://kroki.io
    - Skill: packages/skills-library/main/diagram-generator/SKILL.md
"""

import base64
import zlib
from pathlib import Path
from typing import Literal, Optional
import urllib.request
import urllib.error

# Type aliases for supported formats
DiagramType = Literal["mermaid", "plantuml", "graphviz", "d2", "structurizr", "ditaa", "erd", "nomnoml"]
OutputFormat = Literal["png", "svg", "pdf"]


class DiagramError(Exception):
    """Error during diagram generation."""
    pass


def _encode_diagram(code: str) -> str:
    """
    Compress and base64-encode diagram code for Kroki URL.

    Args:
        code: Raw diagram code (Mermaid, PlantUML, etc.)

    Returns:
        URL-safe base64-encoded compressed string
    """
    compressed = zlib.compress(code.encode('utf-8'), 9)
    encoded = base64.urlsafe_b64encode(compressed).decode('ascii')
    return encoded


def generate_diagram(
    diagram_code: str,
    output_path: str,
    diagram_type: DiagramType = "mermaid",
    output_format: OutputFormat = "png",
    timeout: int = 30
) -> str:
    """
    Generate a diagram using Kroki API.

    Args:
        diagram_code: Text-based diagram code (Mermaid, PlantUML, etc.)
        output_path: Where to save the output file
        diagram_type: Diagram language (default: mermaid)
        output_format: Output format (default: png)
        timeout: Request timeout in seconds (default: 30)

    Returns:
        Absolute path to the saved diagram file

    Raises:
        DiagramError: If generation fails (invalid syntax, network error, etc.)

    Example:
        >>> code = '''
        ... flowchart TD
        ...     A[Start] --> B{Decision}
        ...     B -->|Yes| C[Done]
        ...     B -->|No| D[Retry]
        ... '''
        >>> path = generate_diagram(code, "exports/flowchart.png")
        >>> print(f"Saved to: {path}")
    """
    # Validate inputs
    if not diagram_code.strip():
        raise DiagramError("Empty diagram code provided")

    # Encode the diagram
    encoded = _encode_diagram(diagram_code)

    # Build Kroki URL
    url = f"https://kroki.io/{diagram_type}/{output_format}/{encoded}"

    # Fetch the diagram
    try:
        request = urllib.request.Request(
            url,
            headers={"Accept": f"image/{output_format}"}
        )
        with urllib.request.urlopen(request, timeout=timeout) as response:
            content = response.read()
    except urllib.error.HTTPError as e:
        if e.code == 400:
            raise DiagramError(
                f"Invalid {diagram_type} syntax. Check your diagram code. "
                f"API response: {e.read().decode('utf-8', errors='replace')}"
            )
        raise DiagramError(f"Kroki API error (HTTP {e.code}): {e.reason}")
    except urllib.error.URLError as e:
        raise DiagramError(f"Network error connecting to Kroki: {e.reason}")
    except TimeoutError:
        raise DiagramError(f"Kroki API request timed out after {timeout}s")

    # Validate response has content
    if len(content) < 100:
        raise DiagramError(f"Received unexpectedly small response ({len(content)} bytes)")

    # Save to file
    output = Path(output_path)
    try:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(content)
    except OSError as e:
        raise DiagramError(f"Failed to write file: {e}")

    return str(output.absolute())


def generate_mermaid(
    mermaid_code: str,
    output_path: str,
    output_format: OutputFormat = "png"
) -> str:
    """
    Convenience function for generating Mermaid diagrams.

    Args:
        mermaid_code: Mermaid diagram code
        output_path: Where to save the output
        output_format: png, svg, or pdf (default: png)

    Returns:
        Absolute path to saved file

    Example:
        >>> code = "flowchart LR\\n    A --> B"
        >>> generate_mermaid(code, "diagram.png")
    """
    return generate_diagram(
        mermaid_code,
        output_path,
        diagram_type="mermaid",
        output_format=output_format
    )


def get_diagram_url(
    diagram_code: str,
    diagram_type: DiagramType = "mermaid",
    output_format: OutputFormat = "png"
) -> str:
    """
    Get Kroki URL without downloading (useful for embedding in markdown).

    Args:
        diagram_code: Diagram code
        diagram_type: Diagram language
        output_format: Output format

    Returns:
        Full Kroki URL that can be used as image source

    Example:
        >>> url = get_diagram_url("flowchart LR\\n    A --> B")
        >>> print(f"![Diagram]({url})")
    """
    encoded = _encode_diagram(diagram_code)
    return f"https://kroki.io/{diagram_type}/{output_format}/{encoded}"


# CLI interface
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python kroki.py <input_file> <output_file> [diagram_type] [format]")
        print("Example: python kroki.py diagram.mmd output.png mermaid png")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    dtype = sys.argv[3] if len(sys.argv) > 3 else "mermaid"
    fmt = sys.argv[4] if len(sys.argv) > 4 else "png"

    try:
        with open(input_file) as f:
            code = f.read()
        result = generate_diagram(code, output_file, dtype, fmt)
        print(f"Generated: {result}")
    except DiagramError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: Input file not found: {input_file}", file=sys.stderr)
        sys.exit(1)
