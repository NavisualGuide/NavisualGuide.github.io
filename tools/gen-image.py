"""Generate or edit an image with Gemini and save it as PNG.

    python tools/gen-image.py OUT.png "prompt" [--aspect 21:9] [--edit IN.png]
                              [--model gemini-3.1-flash-image]

--edit sends IN.png with the prompt, so the model changes that image instead of
drawing a new one: the way to fix one detail without losing a composition.

--aspect is one of Gemini's ratios (1:1, 3:2, 16:9, 21:9, ...). 5:2 is not one
of them, so for a hero ask for 21:9 and fit it with hero_common's W x H.

Use it for illustration and atmosphere. For anything carrying exact words or
the site's exact colours, draw it with Pillow instead (hero_common.py): image
models garble small text and cannot hit a given hex value. And read what comes
back: asked for "a hand on a mouse about to click", it drew a hand holding a
mouse AND poking the screen.

The key is read from GEMINI_API_KEY and never written anywhere. Every call
bills the owner's Google account.
"""
import argparse, base64, json, os, sys, urllib.error, urllib.request

ap = argparse.ArgumentParser()
ap.add_argument("out")
ap.add_argument("prompt")
ap.add_argument("--aspect", default="16:9")
ap.add_argument("--edit")
ap.add_argument("--model", default="gemini-3.1-flash-image")
a = ap.parse_args()

parts = []
if a.edit:
    parts.append({"inlineData": {"mimeType": "image/png",
                                 "data": base64.b64encode(open(a.edit, "rb").read()).decode()}})
parts.append({"text": a.prompt})

body = {
    "contents": [{"parts": parts}],
    "generationConfig": {"responseModalities": ["IMAGE"],
                         "imageConfig": {"aspectRatio": a.aspect}},
}
req = urllib.request.Request(
    f"https://generativelanguage.googleapis.com/v1beta/models/{a.model}:generateContent",
    data=json.dumps(body).encode(),
    headers={"Content-Type": "application/json", "x-goog-api-key": os.environ["GEMINI_API_KEY"]})
try:
    resp = json.load(urllib.request.urlopen(req, timeout=180))
except urllib.error.HTTPError as e:
    sys.exit(f"HTTP {e.code}: {e.read().decode()[:400]}")

for part in resp.get("candidates", [{}])[0].get("content", {}).get("parts", []):
    if "inlineData" in part:
        open(a.out, "wb").write(base64.b64decode(part["inlineData"]["data"]))
        print(f"{a.out}  {a.model}  {resp.get('usageMetadata', {}).get('totalTokenCount')} tokens")
        break
else:
    sys.exit("no image in response: " + json.dumps(resp)[:400])
