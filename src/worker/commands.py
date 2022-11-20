from typing import Any

import typer

from src.common.start_up import on_startup
from src.common.utils import run_async
from src.containers.container import container

app = typer.Typer()


@app.command()
@run_async
async def mailing(self: Any, msg: str) -> None:
    await on_startup()
    bot_repo = await container.repos.bot_repo()
    async with bot_repo as bot:
        await bot.send_message_all(msg)


if __name__ == "__main__":
    app()