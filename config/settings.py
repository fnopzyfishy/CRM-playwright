import os
from enum import Enum
from pathlib import Path
from typing import Self

from pydantic import Field, HttpUrl, model_validator, BaseModel, NonNegativeInt, PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict


class Browser(str, Enum):
    CHROMIUM = 'chromium'
    FIREFOX = 'firefox'
    WEBKIT = 'webkit'


class LoggingLevel(str, Enum):
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'


class Environment(str, Enum):
    LOCAL = 'local'
    STAGING = 'staging'
    PRODUCTION = 'production'


class TestUser(BaseModel):
    username: str
    password: str


class BrowserSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='BROWSER_')
    
    browser_type: Browser = Field(default=Browser.CHROMIUM)
    headless: bool = Field(default=True)
    slow_mo: NonNegativeInt = Field(default=0)
    width: PositiveInt = Field(default=1920)
    height: PositiveInt = Field(default=1080)
    
    @model_validator(mode='after')
    def check_dimensions(self) -> Self:
        from config.validators import validate_browser_dimensions
        validate_browser_dimensions(self)
        return self


class TimeoutSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='TIMEOUT_')
    
    page_load: PositiveInt = Field(default=30000)
    element_wait: PositiveInt = Field(default=10000)
    network_idle: PositiveInt = Field(default=10000)
    api_response: PositiveInt = Field(default=5000)


class LoggingSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='LOGGING_')
    
    level: LoggingLevel = Field(default=LoggingLevel.INFO)
    directory: Path = Field(default=Path('./logs'))


class DirectorySettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='TEST_DIR_')
    
    videos_dir: Path = Field(default=Path('./videos'))
    tracing_dir: Path = Field(default=Path('./tracing'))
    allure_results_dir: Path = Field(default=Path('./allure-results'))


class Settings(BaseSettings):
    _env_name: str = os.getenv("ENV", "")
    _env_file: str = f".env.{_env_name}" if _env_name else ".env"
    
    model_config = SettingsConfigDict(
        env_file=_env_file,
        env_prefix='SETTINGS_',
        env_nested_delimiter='__',
        extra='ignore'
    )
    
    base_url: HttpUrl = Field(default='https://opensource-demo.orangehrmlive.com/')
    environment: Environment = Field(default=Environment.PRODUCTION)
    browser: BrowserSettings = Field(default_factory=BrowserSettings)
    timeout: TimeoutSettings = Field(default_factory=TimeoutSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    directories: DirectorySettings = Field(default_factory=DirectorySettings)
    test_user: TestUser = Field(default_factory=lambda: TestUser(username='Admin', password='admin123'))
    
    @property
    def base_url_str(self) -> str:
        return str(self.base_url)
    
    @model_validator(mode='after')
    def check_all(self) -> Self:
        from config.validators import validate_environment_rules
        validate_environment_rules(self)
        return self


settings = Settings()
