import sys, json, asyncio, cognee

async def main():
    data = json.load(sys.stdin)
    prompt = data.get("prompt", "")
    if not prompt.strip():
        return
    try:
        results = await cognee.recall(query_text=prompt)
        text = "\n".join(getattr(r, "text", str(r)) for r in results)
    except Exception:
        return
    if text.strip():
        print("=== PROJECT MEMORY (past decisions) ===")
        print(text)
        print("=== GUARDRAIL RULE ===")
        print("If my request conflicts with any REJECTED APPROACH above, STOP and warn me, citing the past decision. Otherwise continue normally.")

asyncio.run(main())