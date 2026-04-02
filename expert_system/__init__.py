"""Computer maintenance expert system package."""

from .knowledge_base import KNOWLEDGE_BASE


def run_app() -> None:
    from .ui import run_app as desktop_run_app

    desktop_run_app()


def create_app():
    from .web import create_app as web_create_app

    return web_create_app()


__all__ = ["KNOWLEDGE_BASE", "run_app", "create_app"]
