from functools import cache

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class ActionInput(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="input_")

    # ===== auth inputs =====
    # github app
    app_id: str | None = None
    private_key: str | None = None

    # oauth app
    client_id: str | None = None
    client_secret: str | None = None

    # ===== main inputs =====
    script: str

    # ===== debug inputs =====
    debug: bool = False

    @model_validator(mode="after")
    def check_auth(self):
        # if github app, app id or client id must be provided
        if self.app_id or self.private_key:
            if not self.app_id or not self.client_id:
                raise ValueError(
                    "Partial github app authentication information provided."
                )
        # if oauth app
        elif self.client_id or self.client_secret:  # noqa: SIM102
            if not self.client_id or not self.client_secret:
                raise ValueError(
                    "Partial oauth app authentication information provided."
                )
        return self


class ActionContext(BaseSettings): ...


@cache
def get_action_input() -> ActionInput:
    return ActionInput()  # pyright: ignore[reportCallIssue]


@cache
def get_action_context() -> ActionContext:
    return ActionContext()
