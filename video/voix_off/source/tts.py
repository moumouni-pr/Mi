import sys, os, json, base64, urllib.request, wave
voice, out, model = sys.argv[1], sys.argv[2], sys.argv[3]
d = os.path.dirname(os.path.abspath(out)); txt = open(sys.argv[4]).read().strip(); style = open(sys.argv[5]).read().strip()
prompt = "# AUDIO PROFILE\nNarrateur francophone de mini-documentaire.\n\n## DIRECTOR'S NOTES\n" + style + "\nNe lis à voix haute que le texte placé sous TRANSCRIPT.\n\n## TRANSCRIPT\n" + txt
body = {"contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["AUDIO"], "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent", json.dumps(body).encode(),
                             {"Content-Type": "application/json", "x-goog-api-key": os.environ["GEMINI_API_KEY"]})
try: r = json.load(urllib.request.urlopen(req, timeout=540))
except urllib.error.HTTPError as e: print("ERREUR", e.code, e.read()[:500].decode(errors='replace')); sys.exit(1)
p = r["candidates"][0]["content"]["parts"][0]["inlineData"]; print(p["mimeType"], r.get("usageMetadata", {}).get("totalTokenCount"))
pcm = base64.b64decode(p["data"]); rate = int(p["mimeType"].split("rate=")[1].split(";")[0]) if "rate=" in p["mimeType"] else 24000
with wave.open(out, "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(pcm)
print(out, len(pcm) / 2 / rate, "s")
