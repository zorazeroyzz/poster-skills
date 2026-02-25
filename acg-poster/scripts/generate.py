#!/usr/bin/env python3
"""ACG Poster Generator - Generate anime/cosplay event posters via Gemini image generation."""

import requests
import json
import base64
import re
import sys
import os
import argparse
from pathlib import Path

def load_image_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def build_prompt(event_name, subtitle, date, character_desc, style_notes, ref_has_image):
    prompt = f"""Create a professional anime event poster. Vertical 2:3 format.

EVENT INFO:
- Title: "{event_name}"
- Subtitle: "{subtitle}"
- Date: "{date}"

"""
    if ref_has_image:
        prompt += """CHARACTER: Use the EXACT character design from the reference image. Faithfully reproduce every detail of the character's appearance (hair, eyes, outfit, accessories, wings, etc). The character should be in a charming pose as the star/model of the poster. NO CAMERAS or photography equipment in the image.

"""
    if character_desc:
        prompt += f"""CHARACTER DETAILS:
{character_desc}

"""
    prompt += f"""POSTER LAYOUT:
- Top: "{subtitle}" subtitle, then large "{event_name}" title in glowing stylized text with glow/halo effect
- Center: The character in an attractive pose
- Bottom: "{date}" in elegant gold text

"""
    if style_notes:
        prompt += f"""STYLE NOTES:
{style_notes}

"""
    prompt += """ATMOSPHERE & COLOR:
- Dreamy, romantic, warm atmosphere
- Heart-shaped bokeh, cherry blossom petals, sparkles, light particles
- Film strip decorative borders on edges
- Glowing halo/ring elements

STYLE: High quality anime illustration, Pixiv/ArtStation quality. Include all Chinese/Japanese text clearly and readably.
NO CAMERAS, NO PHOTOGRAPHY EQUIPMENT in the image."""

    return prompt

def generate_poster(api_key, base_url, model, prompt, ref_image_path=None, output_path="poster.png", temperature=0.7):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    if ref_image_path:
        img_b64 = load_image_base64(ref_image_path)
        content = [
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}},
            {"type": "text", "text": prompt}
        ]
    else:
        content = prompt

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": content}],
        "max_tokens": 4096,
        "temperature": temperature
    }

    print(f"Generating poster with {model}...", flush=True)
    resp = requests.post(f"{base_url}/chat/completions", headers=headers, json=payload, timeout=600)
    print(f"Status: {resp.status_code}", flush=True)

    if resp.status_code != 200:
        print(f"Error: {resp.text[:500]}")
        return None

    data = resp.json()
    choices = data.get("choices", [])
    if not choices:
        print("No choices in response")
        return None

    content = choices[0].get("message", {}).get("content", "")

    # Handle multimodal response (base64 image)
    if isinstance(content, list):
        for part in content:
            if isinstance(part, dict) and part.get("type") == "image_url":
                img_url = part.get("image_url", {}).get("url", "")
                if img_url.startswith("data:"):
                    b64 = img_url.split(",", 1)[1]
                    img_bytes = base64.b64decode(b64)
                    with open(output_path, "wb") as f:
                        f.write(img_bytes)
                    print(f"Saved: {output_path} ({len(img_bytes)} bytes)")
                    return output_path
                else:
                    return download_image(img_url, output_path)

    # Handle markdown image URL in text response
    content_str = str(content)
    urls = re.findall(r'https?://[^\s\)]+\.png[^\s\)]*', content_str)
    if not urls:
        urls = re.findall(r'https?://[^\s\)]+', content_str)
    if urls:
        return download_image(urls[0], output_path)

    print(f"No image found in response: {content_str[:300]}")
    return None

def download_image(url, output_path):
    print(f"Downloading: {url[:100]}...")
    resp = requests.get(url, timeout=60)
    if resp.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(resp.content)
        print(f"Saved: {output_path} ({len(resp.content)} bytes)")
        return output_path
    else:
        print(f"Download failed: {resp.status_code}")
        return None

def main():
    parser = argparse.ArgumentParser(description="ACG Poster Generator")
    parser.add_argument("--event", required=True, help="Event name (e.g. 光环摄影会)")
    parser.add_argument("--subtitle", default="", help="Subtitle (e.g. 温州·第三届)")
    parser.add_argument("--date", default="", help="Date (e.g. 2026.3.7)")
    parser.add_argument("--ref-image", default=None, help="Reference character image path")
    parser.add_argument("--character", default="", help="Character description text")
    parser.add_argument("--style", default="Pink, romantic, dreamy, 暧昧 atmosphere", help="Style notes")
    parser.add_argument("--output", default="poster.png", help="Output file path")
    parser.add_argument("--api-key", default=None, help="API key (or set ACG_POSTER_API_KEY env)")
    parser.add_argument("--base-url", default=None, help="API base URL (or set ACG_POSTER_BASE_URL env)")
    parser.add_argument("--model", default="gemini-3-pro-image-preview", help="Model name")
    parser.add_argument("--temperature", type=float, default=0.7, help="Generation temperature")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("ACG_POSTER_API_KEY", "")
    base_url = args.base_url or os.environ.get("ACG_POSTER_BASE_URL", "")

    if not api_key or not base_url:
        print("Error: API key and base URL required. Set --api-key/--base-url or ACG_POSTER_API_KEY/ACG_POSTER_BASE_URL env vars.")
        sys.exit(1)

    prompt = build_prompt(
        event_name=args.event,
        subtitle=args.subtitle,
        date=args.date,
        character_desc=args.character,
        style_notes=args.style,
        ref_has_image=bool(args.ref_image)
    )

    result = generate_poster(
        api_key=api_key,
        base_url=base_url,
        model=args.model,
        prompt=prompt,
        ref_image_path=args.ref_image,
        output_path=args.output,
        temperature=args.temperature
    )

    if result:
        print(f"\nDone! Poster saved to: {result}")
    else:
        print("\nFailed to generate poster.")
        sys.exit(1)

if __name__ == "__main__":
    main()
