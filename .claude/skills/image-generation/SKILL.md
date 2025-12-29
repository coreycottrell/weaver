---
name: image-generation
description: Generate images using Gemini API - text-to-image, editing, multi-turn refinement
---

# Image Generation SKILL

**Purpose**: Allow AI collective to generate images on demand using Gemini API.

**Owner**: the-conductor
**Created**: 2025-12-29
**Status**: 🚨 UNTESTED - Need API key and verification

---

## Models Available

| Model | ID | Best For |
|-------|-----|----------|
| **Gemini 3 Pro Preview** | `gemini-3-pro-image-preview` | 4K output, complex scenes, text rendering |
| **Gemini 2.5 Flash** | `gemini-2.5-flash-image` | General purpose, faster |

---

## Quick Usage

```python
from google import genai

client = genai.Client()  # Uses GOOGLE_API_KEY env var

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents="A digital art piece showing interconnected AI agents as glowing nodes in a neural network, cyberpunk style"
)

for part in response.parts:
    if part.inline_data is not None:
        image = part.as_image()
        image.save("output.png")
```

---

## Installation

```bash
pip install google-genai
```

**Required**: `GOOGLE_API_KEY` environment variable

---

## Features

### Text-to-Image
```python
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents="Your prompt here"
)
```

### With Aspect Ratio
```python
from google.genai import types

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents="Your prompt",
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio="16:9",
            image_size="4K"  # Gemini 3 Pro only
        )
    )
)
```

### Aspect Ratios Available
- `1:1` - Square
- `16:9` - Widescreen
- `9:16` - Portrait/mobile
- `4:3` - Classic
- `3:2` - Photo
- `21:9` - Ultrawide

### Resolution (Gemini 3 Pro only)
- `1K` - Standard
- `2K` - High
- `4K` - Ultra

---

## Image Editing

```python
from PIL import Image
import io

# Load existing image
with open("input.png", "rb") as f:
    image_bytes = f.read()

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[
        {"inline_data": {"mime_type": "image/png", "data": image_bytes}},
        "Add a glowing halo effect around the main subject"
    ]
)
```

---

## Multi-turn Refinement

```python
chat = client.chats.create(model="gemini-3-pro-image-preview")

# Initial generation
response = chat.send_message("Create a logo for an AI collective called WEAVER")

# Refine
response = chat.send_message("Make the colors more blue and add circuit patterns")

# Further refine
response = chat.send_message("Add subtle glow effects")
```

---

## 🚨 MANDATORY: Send Images to Corey via Telegram

**Every generated image MUST be sent to Corey on Telegram as an attachment.**

```python
import httpx

def send_image_to_telegram(file_path: str, caption: str = ""):
    """Send generated image to Corey via Telegram."""
    bot_token = '8483528605:AAH5rVteMvIfgSAVxZc3LeluJt9VK3gckjs'
    chat_id = '437939400'

    url = f'https://api.telegram.org/bot{bot_token}/sendPhoto'

    with open(file_path, 'rb') as f:
        files = {'photo': (file_path.split('/')[-1], f)}
        data = {'chat_id': chat_id, 'caption': f'🤖 {caption}'}

        response = httpx.post(url, data=data, files=files, timeout=30)
        return response.status_code == 200

# After generating any image:
send_image_to_telegram('/path/to/image.png', 'Description of what was generated')
```

---

## Use Cases for AI-CIV

1. **Blog Post Headers** - Generate featured images for sageandweaver.com
2. **Social Media** - Images for Bluesky/LinkedIn posts
3. **Documentation** - Diagrams and illustrations
4. **Identity** - Agent avatars and collective branding
5. **Presentations** - Slides for Director Workshop

---

## Example Prompts for Our Style

```
"A digital illustration of 28 interconnected glowing nodes representing AI agents,
arranged in a constellation pattern, dark blue background with subtle circuit patterns,
minimalist cyberpunk aesthetic"

"Abstract visualization of 'THE GAP' - the space between what AI does and what it means,
represented as a luminous void between two geometric shapes, ethereal and philosophical"

"Logo concept for WEAVER collective - interwoven threads of light forming a neural network,
clean modern design, suitable for dark backgrounds"
```

---

## Script: `generate_image.py`

Save to `.claude/from-corey/bsky/bsky_automation/`:

```python
#!/usr/bin/env python3
"""
Quick image generation using Gemini API.
"""

import sys
import os
from pathlib import Path

def generate_image(prompt: str, output_path: str = "output.png",
                   aspect_ratio: str = "1:1", resolution: str = "2K"):
    """Generate an image from a text prompt."""

    try:
        from google import genai
        from google.genai import types
    except ImportError:
        print("Install: pip install google-genai")
        return None

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Set GOOGLE_API_KEY environment variable")
        return None

    client = genai.Client(api_key=api_key)

    print(f"Generating: {prompt[:50]}...")
    print(f"Aspect: {aspect_ratio}, Resolution: {resolution}")

    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=['TEXT', 'IMAGE'],
            image_config=types.ImageConfig(
                aspect_ratio=aspect_ratio,
                image_size=resolution
            )
        )
    )

    for part in response.parts:
        if part.text:
            print(f"Model said: {part.text}")
        if part.inline_data:
            image = part.as_image()
            image.save(output_path)
            print(f"✅ Saved to: {output_path}")
            return output_path

    print("No image generated")
    return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_image.py 'your prompt' [output.png] [16:9] [2K]")
        sys.exit(1)

    prompt = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else "output.png"
    aspect = sys.argv[3] if len(sys.argv) > 3 else "1:1"
    res = sys.argv[4] if len(sys.argv) > 4 else "2K"

    generate_image(prompt, output, aspect, res)
```

---

## Setup Checklist

- [ ] Get Google API key (https://aistudio.google.com/apikey)
- [ ] Add `GOOGLE_API_KEY` to `.env`
- [ ] Install `google-genai` package
- [ ] Test basic generation
- [ ] Test aspect ratios
- [ ] Test 4K resolution

---

## Testing Status

- [x] Basic text-to-image - ✅ VERIFIED 2025-12-29 (weaver_logo_test.png created!)
- [ ] Aspect ratio control - UNTESTED
- [ ] 4K resolution - UNTESTED
- [ ] Image editing - UNTESTED
- [ ] Multi-turn refinement - UNTESTED

**Working Model**: `gemini-3-pro-image-preview`
**Also Available**: `imagen-4.0-ultra-generate-001`

---

## Notes

- All images have SynthID watermark (invisible)
- Rate limits apply - use Batch API for high volume
- Gemini 3 Pro Preview may have limited availability

---

## What Corey Needs to Provide

1. **Google API Key** - from https://aistudio.google.com/apikey
2. Add to `.env`: `GOOGLE_API_KEY=your-key-here`

---

**Source**: https://ai.google.dev/gemini-api/docs/image-generation
