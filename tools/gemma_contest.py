#!/usr/bin/env python3
"""Contest-simulator for the GAITE chatbot: Gemma 4 with a hard 2000-output-token cap.

Reproduces contest conditions (rules PDF v4, Tech Appendix §3):
  - model family: Gemma 4 (`gemma-4-31b-it` by default; the exact contest variant is TBA)
  - max 2000 OUTPUT tokens per query -> enforced via generationConfig.maxOutputTokens,
    so replies TRUNCATE exactly like they will on contest day
  - one call = one fresh chat (no context carried between queries)

Usage:
  export GEMINI_API_KEY=...            # or put the key in a file and pass --key-file
  python3 tools/gemma_contest.py "your prompt"
  python3 tools/gemma_contest.py --model gemma-4-26b-a4b-it --transcript out.md "prompt"
  echo "long prompt" | python3 tools/gemma_contest.py -

Exit codes: 0 ok, 2 reply hit the 2000-token cap (truncated), 1 API error.
"""
import argparse, json, os, sys, time, urllib.error, urllib.request

API = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
CAP = 2000  # GAITE: at most 2000 output tokens per query

def ask(prompt: str, model: str, key: str, retries: int = 4) -> dict:
    body = json.dumps({
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": CAP},
    }).encode()
    req = urllib.request.Request(API.format(model=model, key=key), data=body,
                                 headers={"Content-Type": "application/json"})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            # free API throws intermittent 500/503 -- just resend (drill validation note, 2026-07-11)
            if e.code in (429, 500, 503) and attempt < retries - 1:
                time.sleep(8 * (attempt + 1)); continue
            raise
    raise RuntimeError("unreachable")

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("prompt", help="prompt text, or '-' to read stdin")
    p.add_argument("--model", default="gemma-4-31b-it")
    p.add_argument("--key-file", default=os.environ.get("GEMINI_API_KEY_FILE", ""))
    p.add_argument("--transcript", default="", help="append prompt+reply to this markdown file")
    a = p.parse_args()

    key = os.environ.get("GEMINI_API_KEY", "")
    if not key and a.key_file:
        key = open(a.key_file).read().strip()
    if not key:
        sys.exit("set GEMINI_API_KEY (or --key-file)")

    prompt = sys.stdin.read() if a.prompt == "-" else a.prompt
    resp = ask(prompt, a.model, key)
    cand = resp["candidates"][0]
    text = "".join(part.get("text", "") for part in cand.get("content", {}).get("parts", []))
    fin = cand.get("finishReason", "?")
    usage = resp.get("usageMetadata", {})
    print(text)
    print(f"\n--- [{a.model}] finish={fin} out_tokens={usage.get('candidatesTokensCount') or usage.get('candidatesTokenCount')} "
          f"in_tokens={usage.get('promptTokenCount')}", file=sys.stderr)
    if a.transcript:
        with open(a.transcript, "a") as f:
            f.write(f"\n\n## PROMPT ({a.model}, cap={CAP})\n\n{prompt}\n\n## REPLY (finish={fin})\n\n{text}\n")
    return 2 if fin == "MAX_TOKENS" else 0

if __name__ == "__main__":
    sys.exit(main())
