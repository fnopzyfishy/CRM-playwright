from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from config.settings import BrowserSettings, Settings


def validate_positive_int(value: int, field_name: str) -> None:
    if value < 0:
        raise ValueError(f"'{field_name}' must be >= 0, got {value}")


def validate_browser_dimensions(browser: BrowserSettings) -> None:
    if browser.width < 320:
        raise ValueError('Width must be >= 320px for normal UI rendering')
    if browser.height < 280:
        raise ValueError('Height must be >= 280px for normal UI rendering')
    if browser.width > 7680:
        raise ValueError('Width must be <= 7680px (8K maximum)')

    aspect_ratio = browser.width / browser.height
    if not (1.2 <= aspect_ratio <= 3.0):
        raise ValueError(f'Aspect ratio too extreme: {aspect_ratio:.2f} (allowed: 1.2–3.0)')


def validate_environment_rules(settings: Settings) -> None:
    if settings.environment == 'production':
        if not settings.browser.headless:
            raise ValueError('Headless must be enabled in production')
        if settings.browser.browser_type != 'chromium':
            raise ValueError('Production requires Chromium for stability')
        if settings.browser.slow_mo > 0:
            raise ValueError('slow_mo must be 0 in production')


def validate_url(url: str) -> None:
    if not url or not url.strip():
        raise ValueError('base_url cannot be empty')
    if not (url.startswith('http://') or url.startswith('https://')):
        raise ValueError('base_url must start with http:// or https://')
    if len(url) > 500:
        raise ValueError('base_url is too long (max 500 chars)')