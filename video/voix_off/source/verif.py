"""Retranscrit un MP3 avec Gemini pour vérifier que la voix off dit bien le texte."""
import sys, os, json, base64, urllib.request
b = base64.b64encode(open(sys.argv[1], 'rb').read()).decode()
body = {"contents": [{"parts": [{"text": "Transcris mot pour mot cet audio en français, sans rien corriger ni ajouter. Si un mot anglais ou une indication de ton est prononcé, écris-le tel quel."}, {"inlineData": {"mimeType": "audio/mp3", "data": b}}]}], "generationConfig": {"temperature": 0}}
req = urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent", json.dumps(body).encode(), {"Content-Type": "application/json", "x-goog-api-key": os.environ["GEMINI_API_KEY"]})
try: r = json.load(urllib.request.urlopen(req, timeout=300))
except urllib.error.HTTPError as e: print("ERREUR", e.code, e.read()[:400].decode(errors='replace')); sys.exit(1)
print("".join(p.get("text", "") for p in r["candidates"][0]["content"]["parts"]))
