"""Generate an image with Gemini and save it as PNG.

    GEMINI_API_KEY=... python tools/gen-image.py OUT.png "prompt" [aspect] [model]

aspect: one of Gemini's ratios (1:1, 3:2, 16:9, 21:9, ...). 5:2 is not one of
them, so for a hero ask for 21:9 and crop with hero_common's W x H.

Use it for illustration and atmosphere. For anything carrying exact words or
the site's exact colours, draw it with Pillow instead (hero_common.py): image
models garble small text and cannot hit a given hex value.

The key is read from the environment and never written anywhere. It bills the
owner's Google account per image.
"""
import base64, json, os, sys, urllib.request

out, prompt = sys.argv[1], sys.argv[2]
aspect = sys.argv[3] if len(sys.argv) > 3 else "16:9"
model = sys.argv[4] if len(sys.argv) > 4 else "gemini-3.1-flash-image"
key = os.environ["GEMINI_API_KEY"]

body = {
    "contents": [{"parts": [{"text": prompt}]}],
    "generationConfig": {"responseModalities": ["IMAGE"],
                         "imageConfig": {"aspectRatio": aspect}},
}
req = urllib.request.Request(
    f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
    data=json.dumps(body).encode(),
    headers={"Content-Type": "application/json", "x-goog-api-key": key})
try:
    resp = json.load(urllib.request.urlopen(req, timeout=180))
except urllib.error.HTTPError as e:
    sys.exit(f"HTTP {e.code}: {e.read().decode()[:400]}")

for part in resp.get("candidates", [{}])[0].get("content", {}).get("parts", []):
    if "inlineData" in part:
        open(out, "wb").write(base64.b64decode(part["inlineData"]["data"]))
        print(f"{out}  {model}  {resp.get('usageMetadata', {})}")
        break
else:
    sys.exit("no image in response: " + json.dumps(resp)[:400])
