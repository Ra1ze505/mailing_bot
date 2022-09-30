import asyncio

from loguru import logger

from src.containers.container import container

container.gateways.logging_setup.init()  # type: ignore
scheduler = container.gateways.scheduler()


async def test_scheduler() -> None:
    scheduler.add_job(
        func=print,
        trigger="interval",
        seconds=1,
        args=["Hello World!"],
    )
    print("test_scheduler")
    with open("test.txt", "a") as f:
        f.write("test_scheduler")


scheduler.add_job(
    func=test_scheduler,
    trigger="interval",
    seconds=10,
    replace_existing=True,
    id="test_scheduler",
)


async def start() -> None:
    scheduler.start()
    while True:
        await asyncio.sleep(1)


loop = asyncio.new_event_loop()
loop.run_until_complete(start())
logger.info("scheduler started")
