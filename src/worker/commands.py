import asyncio
from typing import Awaitable, Optional

import typer
from rich import print
from rich.table import Table

from src.common.start_up import on_startup
from src.common.utils import run_async
from src.containers.container import container
from src.domain.bot.interfaces import IBotRepository
from src.domain.user.dto.base import UserOutSchema
from src.domain.user.interfaces import IUserRepository

app = typer.Typer()


# TODO: refactor me
@app.command()
@run_async
async def mailing(
    msg: str,
    ids: Optional[list[int]] = typer.Option(None),
    usernames: Optional[list[str]] = typer.Option(None),
) -> None:

    if ids and usernames:
        print("You need choise only one ids or usernames")
        raise typer.Abort()

    user_repo: IUserRepository = container.repos.user_repo()
    users: list[UserOutSchema] = []

    if ids:
        users = await user_repo.filter_by_chat_ids(ids)
        if len(users) != len(ids):
            diff = set(ids) - set(user.chat_id for user in users)
            print(f'Can`t find users with ids: [bold yellow]{", ".join(diff)}')  # type: ignore
            typer.confirm("Continue", abort=True)

    elif usernames:
        users = await user_repo.filter_by_usernames(usernames)
        if len(users) != len(usernames):
            diff = set(usernames) - set(user.username for user in users)  # type: ignore
            print(f'Can`t find users with usernames: [bold yellow]{", ".join(diff)}')  # type: ignore
            typer.confirm("Continue", abort=True)

    else:
        users = await user_repo.get_all()

    table = Table("id", "username", title="Users", show_lines=True)
    for user in users:
        table.add_row(str(user.chat_id), user.username)

    print(table)

    print(f"You want send msg:\n[bold green]{msg}")
    typer.confirm("", abort=True)

    async def send_task(coro: Awaitable, username: str | None) -> None:
        try:
            await coro
            print(f"[bold green]Send to {username}")
        except Exception as e:
            print(f"[bold red]Fail send to {username}: {e}")

    bot_repo: IBotRepository = container.repos.bot_repo()
    tasks = [send_task(bot_repo.send_message(user.chat_id, msg), user.username) for user in users]

    await asyncio.gather(*tasks)


@app.command()
@run_async
async def parse() -> None:
    await on_startup()
    parse_repo = await container.use_cases.parse_current_rate()
    res = await parse_repo()


if __name__ == "__main__":
    app()
