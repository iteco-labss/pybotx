from typing import TYPE_CHECKING, Callable, Dict, List, Type, cast

from loguru import logger

from .core import BotXDependencyFailure
from .dependencies import solve_dependencies
from .helpers import call_function_as_coroutine
from .models import CommandCallback, Dependency, Message

if TYPE_CHECKING:  # pragma: no cover
    from .bots import BaseBot


async def _handle_exception(
    exceptions_map: Dict[Type[Exception], Callable],
    exc: Exception,
    message: Message,
    bot: "BaseBot",
) -> bool:
    for cls in cast(List[Type[Exception]], type(exc).mro()):
        if cls in exceptions_map:
            exc_catcher = exceptions_map[cls]

            try:
                await call_function_as_coroutine(exc_catcher, exc, message, bot)
                return True
            except Exception as catcher_exc:
                exceptions_map = exceptions_map.copy()
                exceptions_map.pop(cls)
                catching_basic_exc_res = await _handle_exception(
                    exceptions_map, exc, message, bot
                )
                catching_catcher_exc_res = await _handle_exception(
                    exceptions_map, catcher_exc, message, bot
                )
                if catching_basic_exc_res and catching_catcher_exc_res:
                    return True
                logger.exception(
                    f"uncaught exception {catcher_exc !r} during catching {exc !r}"
                )

    return False


async def execute_callback_with_exception_catching(
    exceptions_map: Dict[Type[Exception], Callable], callback: CommandCallback
) -> None:
    message, bot = callback.args[:2]
    callback.args = callback.args[2:]

    try:
        for dep in callback.background_dependencies:
            dep_deps = await solve_dependencies(message, bot, dep)
            await call_function_as_coroutine(dep.call, **dep_deps)

        callback_deps = await solve_dependencies(
            message, bot, Dependency(call=callback.callback)
        )
        await call_function_as_coroutine(
            callback.callback, *callback.args, **callback.kwargs, **callback_deps
        )
    except BotXDependencyFailure:
        pass
    except Exception as exc:
        catcher_res = await _handle_exception(exceptions_map, exc, message, bot)
        if not catcher_res:
            logger.exception(f"uncaught exception {exc !r}")
