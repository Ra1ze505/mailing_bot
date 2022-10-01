import typer

from src.common.utils import run_async

app = typer.Typer()


@app.command()
@run_async
async def hello(name: str) -> None:
    print(f"Hello {name}")


@app.command()
def goodbye(name: str, formal: bool = False) -> None:
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")


if __name__ == "__main__":
    app()
