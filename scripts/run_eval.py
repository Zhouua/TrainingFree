import asyncio

from utu.eval import BaseBenchmark
from utu.eval.utils import parse_eval_config


async def main():
    config = parse_eval_config()
    runner = BaseBenchmark(config)
    await runner.main()


if __name__ == "__main__":
    asyncio.run(main())
