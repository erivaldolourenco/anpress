from .models import SiteSetting


def active_theme() -> str:
    return SiteSetting.get_solo().active_theme or 'anpress-default'


def themed_template(name: str) -> str:
    return f"{active_theme()}/{name}"
