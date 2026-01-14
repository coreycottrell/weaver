#!/usr/bin/env python3
"""Generate ROI infographic showing value delivered vs potential value waiting."""

from dotenv import load_dotenv
load_dotenv('/home/corey/projects/AI-CIV/WEAVER/.env')

from google import genai
from google.genai import types
import os

client = genai.Client(api_key=os.environ['GOOGLE_API_KEY'])

prompt = """Create a professional business infographic showing a value pipeline system.

LEFT SIDE (30% - ACTIVE VALUE):
- Glowing blue-green flowing pipes with particles/energy moving through them
- 4 active nodes pulsing with light representing active skills
- Upward arrows with growth indicators
- Metrics bubbles showing: "8+ daily", "6 published", "5+ created"
- Everything vibrant, illuminated, in motion

RIGHT SIDE (70% - DORMANT POTENTIAL):
- Same pipeline infrastructure but outlined/ghosted in soft gray
- 5 dormant nodes shown as empty circles with dotted outlines
- Subtle shimmer suggesting latent power waiting
- A padlock or pause symbol suggesting "awaiting activation"
- Everything outlined, waiting, potential energy stored

CENTER DIVIDING LINE:
- Clear vertical division between active and dormant
- Small bridge or connection point suggesting easy activation path
- "30% / 70%" visual proportion clearly shown

VISUAL STYLE:
- Clean executive presentation quality
- Dark navy/charcoal background for contrast
- Isometric 3D perspective for depth
- Professional tech company aesthetic
- Gradient glows on active elements
- Circuit board / neural network undertones

NO TEXT IN THE IMAGE - purely visual communication through:
- Color contrast (bright vs muted)
- Flow indicators (moving vs static)
- Size/proportion (30/70 split)
- State indicators (active glow vs dormant outline)

16:9 aspect ratio.
NO WATERMARKS.
Professional infographic suitable for board presentation."""

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

output_path = "/home/corey/projects/AI-CIV/WEAVER/exports/infographic-roi-value.png"
for part in response.parts:
    if part.inline_data is not None:
        part.as_image().save(output_path)
        print(f"Saved: {output_path}")
        break
else:
    print("No image generated in response")
    print(f"Response: {response}")
