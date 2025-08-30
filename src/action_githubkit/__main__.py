import asyncio
import logging

from .config import get_action_context, get_action_input
from .github import get_client
from .script import parse_script, run_script

logger = logging.getLogger(__name__)


async def main():
    action_input = get_action_input()
    action_context = get_action_context()

    logging.basicConfig(level=logging.DEBUG if action_input.debug else logging.INFO)

    try:
        client = await get_client()
        script = parse_script(action_input.script)
        globalns = {
            # githubkit client
            "g": client,
            "github": client,
            # action inputs
            "action_input": action_input,
            # action context info
            "action_context": action_context,
        }
        run_script(script, globals=globalns)
    except Exception:
        logger.exception("Job failed to complete. See the error below:")
        exit(1)


asyncio.run(main())
