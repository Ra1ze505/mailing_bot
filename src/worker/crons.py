import argparse
import asyncio

from src.containers.container import container


async def mailing() -> None:
    bulk_mailing = await container.use_cases.bulk_mailing()
    await bulk_mailing()


async def parse() -> None:
    parse_news = await container.use_cases.parse_last_news()
    parse_rate = container.use_cases.parse_current_rate()
    tasks = [parse_news(), parse_rate()]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    container.gateways.logging_setup.init()  # type: ignore
    parser = argparse.ArgumentParser(description="Run tasks")
    parser.add_argument(
        "-n", "--name", help="Name task to run", choices=["mailing", "parse"], required=True
    )
    args = parser.parse_args()

    loop = asyncio.get_event_loop()

    match args.name:
        case "mailing":
            loop.run_until_complete(mailing())

        case "parse":
            loop.run_until_complete(parse())
