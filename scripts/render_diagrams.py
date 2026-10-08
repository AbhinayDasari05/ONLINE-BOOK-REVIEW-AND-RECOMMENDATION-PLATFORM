import os
import sys
import base64
import requests
from diagram_sources import DIAGRAMS

OUTPUT_DIR = "/Users/abhinaydasari/Documents/sse/secure-book-review-platform/diagrams"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"[*] Generating diagrams into {OUTPUT_DIR}...")

for name, mermaid_code in DIAGRAMS.items():
    clean_code = mermaid_code.strip()
    
    # 1. Save .mmd source file
    mmd_path = os.path.join(OUTPUT_DIR, f"{name}.mmd")
    with open(mmd_path, "w", encoding="utf-8") as f:
        f.write(clean_code)
    print(f"  [+] Saved source: {name}.mmd")

    # 2. Fetch PNG from mermaid.ink
    try:
        encoded = base64.urlsafe_b64encode(clean_code.encode("utf-8")).decode("ascii")
        img_url = f"https://mermaid.ink/img/{encoded}"
        resp = requests.get(img_url, timeout=15)
        
        if resp.status_code == 200 and len(resp.content) > 100:
            png_path = os.path.join(OUTPUT_DIR, f"{name}.png")
            with open(png_path, "wb") as f:
                f.write(resp.content)
            print(f"  [✓] Generated PNG: {name}.png ({len(resp.content)} bytes)")
        else:
            # Try SVG endpoint
            svg_url = f"https://mermaid.ink/svg/{encoded}"
            svg_resp = requests.get(svg_url, timeout=15)
            if svg_resp.status_code == 200:
                svg_path = os.path.join(OUTPUT_DIR, f"{name}.svg")
                with open(svg_path, "wb") as f:
                    f.write(svg_resp.content)
                print(f"  [✓] Generated SVG: {name}.svg ({len(svg_resp.content)} bytes)")
            else:
                print(f"  [!] Remote render returned HTTP {resp.status_code} for {name}")
    except Exception as e:
        print(f"  [-] Error downloading render for {name}: {e}")

print("[*] Diagram generation finished.")
