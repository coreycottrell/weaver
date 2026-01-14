#!/usr/bin/env python3
"""Generate Ecosystem Completion Recommendations Infographic"""

from dotenv import load_dotenv
load_dotenv('/home/corey/projects/AI-CIV/WEAVER/.env')

from google import genai
from google.genai import types
import os

client = genai.Client(api_key=os.environ['GOOGLE_API_KEY'])

prompt = """Professional infographic: ECOSYSTEM COMPLETION RECOMMENDATIONS

TITLE: "Completing the Loop: From Clusters to Ecosystem"

TOP SECTION - "CURRENT STATE vs TARGET STATE"
Left side: "NOW - Disconnected"
• 3 active clusters
• 1 dormant cluster (Content Pipeline)
• Manual coordination between clusters

Right side: "TARGET - Unified Ecosystem"
• All 4 clusters active
• Automatic flow between them
• Self-sustaining loop

MIDDLE SECTION - "3 RECOMMENDATIONS"
1. "ACTIVATE CLUSTER 3"
   • "Configure content pipeline crons"
   • "Unlocks: intel-scan → deep-research → daily-blog → verify-publish → evening-capture"

2. "CONNECT THE LOOP"
   • "Wire: Content → Publishing → Bluesky → Research"
   • "Creates: Self-reinforcing cycle"

3. "STRENGTHEN FOUNDATION"
   • "Add monitoring to core skills"
   • "Ensures: Ecosystem health visibility"

BOTTOM SECTION - "THE COMPLETE LOOP"
Circular diagram showing all 4 clusters connected:
"Cluster 3: Research & Content"
  ↓
"Cluster 2: Publishing"
  ↓
"Cluster 1: Bluesky Engagement"
  ↓
"Insights & Ideas"
  ↓
(back to Cluster 3)

"Cluster 4: Foundation" supporting all in the center

COMPOUNDING EFFECTS CALLOUT:
"Each cycle strengthens the next"
• "Better research → Better content"
• "Better content → More engagement"
• "More engagement → More insights"
• "More insights → Better research"

STYLE: Systems thinking, interconnected.
Dark background with glowing connections.
Circular flow emphasized.
Professional architecture aesthetic.
16:9 aspect ratio."""

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_modalities=['IMAGE'],
        image_config=types.ImageConfig(aspect_ratio="16:9", image_size="2K"),
    )
)

saved = False
for part in response.parts:
    if part.inline_data is not None:
        part.as_image().save("/home/corey/projects/AI-CIV/WEAVER/exports/infographic-recommendations-ecosystem.png")
        print("Saved: /home/corey/projects/AI-CIV/WEAVER/exports/infographic-recommendations-ecosystem.png")
        saved = True

if not saved:
    print("ERROR: No image generated")
    if hasattr(response, 'text'):
        print(f"Response text: {response.text}")
