from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings
from typing import Literal

from config.validators import validate_url


class BrowserSettings(BaseSettings):
    browser_type: Literal['chromium', 'firefox', 'webkit'] = Field(
        default='chromium',
        description='Browser type',
    )
    headless: bool = Field(
        default=True,
        description='Headless format',
    )
    slow_mo: int = Field(
        default=0,
        description='Slow mo actions(ms)',
    )
    width: int = Field(
        default=1920,
        description='Width of browser window',
    )
    height: int = Field(
        default=1080,
        description='Heigh of browser window',
    )
    
    @field_validator('slow_mo', 'width', 'height')
    @classmethod
    def validate_positive(cls, v):
        if v < 0:
            raise ValueError(f'{v} must be a positive integer')
        return v
    
    @model_validator(mode='after')
    def validate_dimensions(self):
        from config.validators import validate_browser_dimensions
        validate_browser_dimensions(self)
        return self

    class Config:
        env_prefix = 'BROWSER_'


class TimeoutSettings(BaseSettings):
    page_load: int = Field(
        default=30000,
        description='Page load timeout (ms)',
    )
    element_wait: int = Field(
        default=10000,
        description='Element wait timeout (ms)',
    )
    networkidle_load: int = Field(
        default=10000,
        description='Timeout networkidle (ms)',
    )
    api_response_timeout: int = Field(
        default=5000,
        description='API response timeout (ms)',
    )
    
    @field_validator('page_load', 'element_wait', 'networkidle_load', 'api_response_timeout')
    @classmethod
    def validate_positive(cls, v):
        if v < 0:
            raise ValueError(f'{v} must be a positive integer')
        return v

    class Config:
        env_prefix = 'TIMEOUT_'


class LoggingSettings(BaseSettings):
    level: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR'] = Field(
        default='INFO',
        description='Logging level',
    )
    directory: str = Field(
        default='./logs',
        description='Directory for log files',
    )

    class Config:
        env_prefix = 'LOGGING_'


class Settings(BaseSettings):
    base_url: str = Field(default='https://opensource-demo.orangehrmlive.com/', description='Default url')
    environment: Literal['local', 'staging', 'production'] = Field(default='local', description='Test environment')
    browser: BrowserSettings = Field(default_factory=BrowserSettings)
    timeout: TimeoutSettings = Field(default_factory=TimeoutSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)

    @model_validator(mode='after')
    def validate_all(self):
        from config.validators import validate_all_settings
        validate_all_settings(self)
        validate_url(self.base_url)
        return self

    class Config:
        env_file = '.env'
        env_prefix = 'SETTING_'
        env_nested_delimiter = '__'


settings = Settings()