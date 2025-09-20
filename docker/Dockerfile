FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:0.8 /uv /bin/uv

COPY . /app/

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  --mount=type=cache,target=/root/.cache/uv,sharing=locked \
  rm -f /etc/apt/apt.conf.d/docker-clean && \
  echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' >/etc/apt/apt.conf.d/keep-cache && \
  UV_COMPILE_BYTECODE=1 UV_FROZEN=1 UV_LINK_MODE=copy uv sync --project /app/ --no-dev

CMD ["UV_COMPILE_BYTECODE=1", "UV_FROZEN=1", "UV_LINK_MODE=copy", "uv", "run", "--project", "/app/", "--no-dev", "-m", "action_githubkit"]
