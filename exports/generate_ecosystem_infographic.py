#!/usr/bin/env python3
"""Generate text-dense skill ecosystem infographic using Gemini 3 Pro Image."""

from dotenv import load_dotenv
load_dotenv('/home/corey/projects/AI-CIV/WEAVER/.env')

from google import genai
from google.genai import types
import os

client = genai.Client(api_key=os.environ['GOOGLE_API_KEY'])

prompt = """Professional text-dense infographic: SKILL ECOSYSTEM ARCHITECTURE

TITLE: "WEAVER Skills: Ecosystem Map - Jan 2026"

FOUR QUADRANT LAYOUT with central hub:

TOP-RIGHT - "CLUSTER 1: BLUESKY" (Green border)
Header: "SOCIAL ENGAGEMENT - ACTIVE"
Skills with descriptions:
• bsky-safety: "Rate limits & ban prevention"
• bsky-engage: "Quality-first protocol"
• bsky-boop-manager: "Hourly notification sweeps"
Status: "✓ FULLY OPERATIONAL"
Metrics: "8+ activations/day"

TOP-LEFT - "CLUSTER 2: PUBLISHING" (Amber border)
Header: "CONTENT DISTRIBUTION - CONSOLIDATING"
• post-blog v2.0: "End-to-end publishing"
  - "← Absorbed: sageandweaver-blog"
  - "← Absorbed: blog-thread-posting"
  - "← Absorbed: verify-publish"
Status: "✓ CONSOLIDATION COMPLETE"
Metrics: "6 blogs this week"

BOTTOM-LEFT - "CLUSTER 3: CONTENT PIPELINE" (Gray border)
Header: "AUTOMATED CONTENT - DORMANT"
Pipeline flow:
"intel-scan (6am) → deep-research (7am) → daily-blog (9am) → verify-publish (11am) → evening-capture (6pm)"
Status: "⚠ INFRASTRUCTURE BUILT, NOT ACTIVATED"
Gap: "Cron triggers missing"

BOTTOM-RIGHT - "CLUSTER 4: FOUNDATION" (Blue border)
Header: "CORE INFRASTRUCTURE - STABLE"
• delegation-spine: "Routes all tasks to specialists"
• image-generation: "Gemini 3 Pro Image"
• image-self-review: "Mandatory quality gate"
Status: "✓ STABLE FOUNDATION"
Note: "All clusters depend on these"

CENTER HUB:
"THE-CONDUCTOR"
"Orchestration Core"
Arrows showing connections between all clusters

BOTTOM INSIGHT:
"Architecture is sound. Cluster 3 activation would complete the ecosystem."

STYLE: Technical architecture diagram with text.
Clean quadrant layout.
Color-coded sections matching cluster status.
Professional IT documentation aesthetic.
16:9 aspect ratio."""

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_modalities=['IMAGE'],
        image_config=types.ImageConfig(aspect_ratio="16:9", image_size="2K"),
    )
)

output_path = "/home/corey/projects/AI-CIV/WEAVER/exports/infographic-ecosystem-map-detailed.png"
for part in response.parts:
    if part.inline_data is not None:
        part.as_image().save(output_path)
        print(f"✅ Saved: {output_path}")
        break
else:
    print("❌ No image generated in response")
    if hasattr(response, 'text'):
        print(f"Response text: {response.text}")
