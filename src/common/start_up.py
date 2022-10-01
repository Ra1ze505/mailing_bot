from loguru import logger

from src.containers.container import container


async def on_startup() -> None:
    await container.init_resources()  # type: ignore
    logger.info("Init resources")
