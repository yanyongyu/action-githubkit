import logging

from .config import get_action_input

action_input = get_action_input()

logging.basicConfig(level=logging.DEBUG if action_input.debug else logging.INFO)
