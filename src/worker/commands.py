import typer
from rich import print

from src.common.start_up import on_startup
from src.common.utils import run_async
from src.containers.container import container

app = typer.Typer()


@app.command()
@run_async
async def hello(name: str) -> None:
    await on_startup()
    weather = await container.repos.weather()

    res = await weather.get_weather_forecast("Moscow")
    print(res)


if __name__ == "__main__":
    app()
