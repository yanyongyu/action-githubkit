import logging

from githubkit import (
    ActionAuthStrategy,
    AppAuthStrategy,
    BaseAuthStrategy,
    Config,
    GitHub,
    OAuthAppAuthStrategy,
)

from .config import get_action_input

logger = logging.getLogger(__name__)


def get_auth_strategy() -> AppAuthStrategy | OAuthAppAuthStrategy | ActionAuthStrategy:
    action_input = get_action_input()

    if action_input.private_key:
        return AppAuthStrategy(
            action_input.app_id,
            action_input.private_key,
            action_input.client_id,
            action_input.client_secret,
        )
    elif action_input.client_id and action_input.client_secret:
        return OAuthAppAuthStrategy(action_input.client_id, action_input.client_secret)

    auth = ActionAuthStrategy()
    return auth


def get_config() -> Config: ...


def get_client[A: BaseAuthStrategy](auth: A, config: Config) -> GitHub[A]:
    return GitHub(auth, config=config)
