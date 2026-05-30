from typing import Literal

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class BrowserSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='BROWSER_')

    browser_type: Literal['chromium', 'firefox', 'webkit'] = Field(
        default='chromium',
        description='Browser type to use',
    )
    headless: bool = Field(default=True)
    slow_mo: int = Field(default=0, description='Delay between actions (ms)')
    width: int = Field(default=1920)
    height: int = Field(default=1080)

    @field_validator('slow_mo', 'width', 'height')
    @classmethod
    def must_be_non_negative(cls, v: int, info) -> int:
        if v < 0:
            raise ValueError(f"'{info.field_name}' must be >= 0, got {v}")
        return v

    @model_validator(mode='after')
    def check_dimensions(self):
        from config.validators import validate_browser_dimensions
        validate_browser_dimensions(self)
        return self


class TimeoutSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='TIMEOUT_')

    page_load: int = Field(default=30000, description='Page load timeout (ms)')
    element_wait: int = Field(default=10000, description='Element wait timeout (ms)')
    network_idle: int = Field(default=10000, description='Network idle timeout (ms)')
    api_response: int = Field(default=5000, description='API response timeout (ms)')

    @field_validator('page_load', 'element_wait', 'network_idle', 'api_response')
    @classmethod
    def must_be_positive(cls, v: int, info) -> int:
        if v <= 0:
            raise ValueError(f"'{info.field_name}' must be > 0, got {v}")
        return v


class LoggingSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='LOGGING_')

    level: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR'] = Field(default='INFO')
    directory: str = Field(default='./logs')


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='SETTINGS_',
        env_nested_delimiter='__',
    )

    base_url: str = Field(default='https://opensource-demo.orangehrmlive.com/')
    environment: Literal['local', 'staging', 'production'] = Field(default='production')
    browser: BrowserSettings = Field(default_factory=BrowserSettings)
    timeout: TimeoutSettings = Field(default_factory=TimeoutSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)

    @model_validator(mode='after')
    def check_all(self):
        from config.validators import validate_url, validate_environment_rules
        validate_url(self.base_url)
        validate_environment_rules(self)
        return self


settings = Settings()