#!/usr/bin/env python3
"""Generate ROI Recommendations Infographic using Gemini 3 Pro Image."""

from dotenv import load_dotenv
load_dotenv('/home/corey/projects/AI-CIV/WEAVER/.env')

from google import genai
from google.genai import types
import os

client = genai.Client(api_key=os.environ['GOOGLE_API_KEY'])

prompt = """Professional business infographic: ROI-DRIVEN RECOMMENDATIONS

TITLE: "Unlocking 70%: The Business Case for Skill Activation"

LEFT COLUMN - "RECOMMENDATIONS BY PRIORITY"
IMMEDIATE (This Week):
- "Configure daily content pipeline crons"
- "Expected: Autonomous daily publishing"

SHORT-TERM (This Month):
- "Add analytics and metrics tracking"
- "Expected: Data-driven optimization"

MEDIUM-TERM (This Quarter):
- "Cross-platform syndication"
- "Expected: Multiplied reach"

CENTER - "COMPOUNDING VALUE TIMELINE"
Visual timeline or growth curve showing:
- Week 1: "Daily automated content begins"
- Month 1: "30 pieces vs 6 manual"
- Month 3: "Established authority"
- Month 6: "Inbound opportunities"
- Year 1: "Recognized ecosystem voice"

RIGHT COLUMN - "ROI PROJECTION"
Before/After comparison:
CURRENT STATE:
- "~6 blogs/week"
- "Manual effort"
- "Reactive publishing"

ACTIVATED STATE:
- "7 blogs/week + engagement + research"
- "Automated pipeline"
- "Proactive presence"
- "5x output, LESS effort"

BOTTOM CALLOUT:
"The Investment: Configure 5 cron jobs (1 hour)"
"The Return: Autonomous thought leadership machine"

STYLE: Executive presentation quality.
Dark navy with gold accents for value.
Growth curves and upward trajectories.
Professional business aesthetic.
16:9 aspect ratio."""

print("Generating ROI Recommendations infographic...")

try:
    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=['IMAGE'],
            image_config=types.ImageConfig(aspect_ratio="16:9", image_size="2K"),
        )
    )

    for part in response.parts:
        if part.inline_data is not None:
            output_path = "/home/corey/projects/AI-CIV/WEAVER/exports/infographic-recommendations-roi.png"
            part.as_image().save(output_path)
            print(f"SUCCESS: Saved to {output_path}")
            break
    else:
        print("ERROR: No image data in response")
        if hasattr(response, 'text'):
            print(f"Response text: {response.text}")

except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
