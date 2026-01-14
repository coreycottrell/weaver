#!/usr/bin/env python3
"""Generate WEAVER Skills Ecosystem Infographic using Gemini 3 Pro Image"""

from dotenv import load_dotenv
load_dotenv('/home/corey/projects/AI-CIV/WEAVER/.env')

from google import genai
from google.genai import types
import os

client = genai.Client(api_key=os.environ['GOOGLE_API_KEY'])

# Ecosystem architecture visualization prompt
prompt = """Create an elegant technology network diagram infographic showing an AI skill ecosystem.

Visual structure:
- Central glowing hub node at center (represents "delegation-spine" - the foundation)
- Three distinct orbital clusters around the hub, each with a different color glow:

CLUSTER 1 (Upper left, CYAN/TEAL glow - ACTIVE):
- 3 interconnected nodes in a triangle formation
- Bright, pulsing energy connections between them
- Represents: safety > engagement > management pipeline

CLUSTER 2 (Upper right, PURPLE/MAGENTA glow - CONSOLIDATING):
- One large node absorbing 3-4 smaller nodes flowing into it
- Merger/consolidation visual effect
- Represents: publishing absorbing blog tools

CLUSTER 3 (Bottom, DIM GREY/BLUE glow - DORMANT):
- 5 nodes in a linear chain/pipeline formation
- Faded, low-energy connections
- Represents: dormant content pipeline

FOUNDATION LAYER (Below all, GOLD glow):
- 3 foundational nodes supporting everything
- Solid, stable connections
- Represents: images, core tools

CONNECTIONS between clusters:
- Dotted energy lines flowing between clusters
- Some bright (active), some dim (potential)
- All connect back to central hub

Style:
- Dark navy/black background with subtle grid
- Bioluminescent, organic tech aesthetic
- Nodes as glowing orbs with soft halos
- Energy flows as particle streams between nodes
- Depth effect with foreground/background layers
- Professional data visualization aesthetic
- Clean, modern, slightly futuristic

16:9 aspect ratio.
NO TEXT, labels, words, or watermarks - pure visual network representation only.
High contrast, crisp detail."""

print("Generating WEAVER Skills Ecosystem infographic...")

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_modalities=['IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio="16:9",
            image_size="2K"
        ),
    )
)

output_path = "/home/corey/projects/AI-CIV/WEAVER/exports/infographic-ecosystem-map.png"
for part in response.parts:
    if part.inline_data is not None:
        part.as_image().save(output_path)
        print(f"Saved: {output_path}")
        break
else:
    print("No image generated in response")
    if hasattr(response, 'text'):
        print(f"Response text: {response.text}")
