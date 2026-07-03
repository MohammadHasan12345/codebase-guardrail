import sys, asyncio, cognee

async def main():
    decision = " ".join(sys.argv[1:])
    if not decision.strip():
        print("Nothing to capture.")
        return
    await cognee.remember(decision)
    print("Captured to project memory:", decision)

asyncio.run(main())