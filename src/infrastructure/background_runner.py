import asyncio
from collections.abc import Callable, Awaitable

class BackgroundRunner:

    def __init__(self):
        self._task: asyncio.Task | None = None

    async def start(self, coro_fn: Callable[[], Awaitable[None]]) -> None:
        self._task = asyncio.create_task(self._guarded(coro_fn))

    async def stop(self) -> None:
        if self._task and (not self._task.done()):
            self._task.cancel()
            await asyncio.gather(self._task, return_exceptions=True)

    async def _guarded(self, coro_fn: Callable[[], Awaitable[None]]) -> None:
        while True:
            try:
                await coro_fn()
            except asyncio.CancelledError:
                break
            except Exception:
                await asyncio.sleep(2)