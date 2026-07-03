import os
import asyncio
from cognee.api.v1.visualize.visualize import visualize_graph


async def main():
    output_path = os.path.abspath("graph.html")
    await visualize_graph(output_path)
    print("Decision graph written to", output_path)


if __name__ == "__main__":
    asyncio.run(main())
