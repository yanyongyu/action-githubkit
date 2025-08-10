import asyncio
import logging

from .config import get_action_input


async def main():
    action_input = get_action_input()

    logging.basicConfig(level=logging.DEBUG if action_input.debug else logging.INFO)

    # client = await get_client()


asyncio.run(main())
