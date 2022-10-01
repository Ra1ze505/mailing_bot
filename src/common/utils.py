from functools import wraps
from typing import Any, Callable, Coroutine, TypeVar, get_type_hints

import anyio
from mypy_extensions import KwArg, VarArg
from pydantic import parse_obj_as

RT = TypeVar("RT")


def serialize(
    func: Callable[..., Coroutine[Any, Any, RT]]
) -> Callable[[VarArg(), KwArg()], Coroutine[Any, Any, RT]]:
    """
    Сериализация ответа функции, используя type hints
    """

    async def wrapper(*args: Any, **kwargs: Any) -> RT:
        results = await func(*args, **kwargs)

        if results:
            return_type = get_type_hints(func).get("return")
            if not return_type:
                raise ValueError("Установите возвращаемый тип функции")
            return parse_obj_as(return_type, results)
        return results

    return wrapper


def get_wind_direction(wind_deg: int) -> str:
    if 337.5 <= wind_deg < 360 or 0 <= wind_deg < 22.5:
        return "северный"
    elif 22.5 <= wind_deg < 67.5:
        return "северо-восточный"
    elif 67.5 <= wind_deg < 112.5:
        return "восточный"
    elif 112.5 <= wind_deg < 157.5:
        return "юго-восточный"
    elif 157.5 <= wind_deg < 202.5:
        return "южный"
    elif 202.5 <= wind_deg < 247.5:
        return "юго-западный"
    elif 247.5 <= wind_deg < 292.5:
        return "западный"
    elif 292.5 <= wind_deg < 337.5:
        return "северо-западный"
    else:
        return "нет данных"


def run_async(func: Callable) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: tuple[Any], **kwargs: dict[str, Any]) -> Any:
        async def coro_wrapper() -> Any:
            return await func(*args, **kwargs)

        return anyio.run(coro_wrapper)

    return wrapper
