import logging

from githubkit import (
    ActionAuthStrategy,
    AppAuthStrategy,
    AppInstallationAuthStrategy,
    Config,
    GitHub,
    OAuthAppAuthStrategy,
)
from githubkit.config import get_config

from .config import get_action_context, get_action_input

logger = logging.getLogger(__name__)


def get_githubkit_auth_strategy() -> (
    AppAuthStrategy | OAuthAppAuthStrategy | ActionAuthStrategy
):
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

    return ActionAuthStrategy()


def get_githubkit_config() -> Config:
    # action_input = get_action_input()
    action_context = get_action_context()
    return get_config(base_url=action_context.api_url)


async def get_client() -> GitHub[
    AppInstallationAuthStrategy | OAuthAppAuthStrategy | ActionAuthStrategy
]:
    action_input = get_action_input()
    auth = get_githubkit_auth_strategy()
    config = get_githubkit_config()

    client = GitHub(auth, config=config)
    if isinstance(client.auth, AppAuthStrategy) and action_input.as_installation:
        action_context = get_action_context()
        try:
            owner, repo = action_context.repository.split("/", 1)
            resp = await client.rest.apps.async_get_repo_installation(owner, repo)
            installation_id = resp.json()["id"]
            client = client.with_auth(client.auth.as_installation(installation_id))
        except Exception:
            logger.exception("Failed to get repo installation")
            raise
    return client  # pyright: ignore[reportReturnType]
