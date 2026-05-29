from config.settings import BrowserSettings, Settings


def validate_browser_dimensions(browser: 'BrowserSettings') -> None:
    if browser.width < 320:
        raise ValueError('Width >= 320px required for normal UI')
    
    if browser.height < 280:
        raise ValueError('Height >= 280px required for normal UI')
    
    if browser.width > 7680:
        raise ValueError('Width <= 7680px (8K maximum)')

    aspect_ratio = browser.width / browser.height
    if aspect_ratio < 1.2 or aspect_ratio > 3:
        raise ValueError(f'Aspect ratio too extreme: {aspect_ratio:.1f}')


def validate_all_settings(settings: 'Settings') -> None:
    # production env settings
    if settings.environment == 'production':
        if not settings.browser.headless:
            raise ValueError(
                'Headless mode must be enabled in production for better performance and stability'
            )
        
        if settings.browser.browser_type != 'chromium':
            raise ValueError('Production environment requires Chromium for best compatibility')
        
        if settings.browser.slow_mo > 0:
            raise ValueError('Production environment should not use slow_mo')
    
    
    # local env settings
    elif settings.environment == 'local':
        if not settings.base_url.startswith('http://localhost'):
            raise ValueError('Local environment should use localhost URL')
    
    
    # staging env settings
    elif settings.environment == 'staging':
        if not settings.base_url.startswith('https://staging'):
            raise ValueError('Staging environment should use staging URL')


def validate_url(url: str) -> None:
    if not url or not url.strip():
        raise ValueError('URL cannot be empty')
    
    if len(url) < 10 or len(url) > 500:
        raise ValueError('URL length must be between 10 and 500 characters')