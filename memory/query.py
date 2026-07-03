import sys, asyncio, cognee

async def main():
    question = " ".join(sys.argv[1:])
    results = await cognee.recall(query_text=question)
    for r in results:
        print(getattr(r, "text", str(r)))

asyncio.run(main())