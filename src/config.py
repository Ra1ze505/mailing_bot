from pathlib import Path

from pydantic import BaseSettings, HttpUrl, validator

BASE_DIR = Path(__file__).parent.parent.parent


START_MESSAGE = """
**Привет!**
Я новостной бот, который будет отправлять вам каждое утро **новости**, **погоду** и **курс валют**!
По умолчанию я отправляю вам новости и погоду в Москве в 8 утра, но ты можешь изменить эти настройки.
Не переживайте за разницу во времени, все будет в порядке.
"""


class EnvBaseSettings(BaseSettings):
    class Config:
        env_file = ".env"


class LoggingSettings(EnvBaseSettings):
    serializer: bool = False
    level: str = "INFO"

    class Config:
        env_prefix = "logging_"


class AppSettings(EnvBaseSettings):
    name: str = ""
    root_path: str = ""
    debug: bool = False
    start_message: str = START_MESSAGE

    class Config:
        env_prefix = "app_"


class BrokerConfig(EnvBaseSettings):
    broker_url: str = "redis://localhost:6379/0"
    broker_api: str = "redis://localhost:6379/0"


class PostgresConfig(EnvBaseSettings):
    scheme: str = "postgresql+asyncpg"
    host: str = "localhost"
    port: str = "5432"
    user: str = "postgres"
    password: str = "postgres"
    db: str = "postgres"
    pool_size: int = 10
    pool_overflow_size: int = 10
    echo: bool = False
    autoflush: bool = False
    autocommit: bool = False
    expire_on_commit: bool = False
    engine_health_check_delay: int = 1
    url: str = ""

    class Config:
        env_prefix = "postgres_"

    @validator("url", pre=True)
    def assemble_url(cls, url: str, values: dict) -> str:
        if not url:
            url = f"{values['scheme']}://{values['user']}:{values['password']}@{values['host']}:{values['port']}/{values['db']}"
        return url


class SentryConfig(EnvBaseSettings):
    dsn: HttpUrl | None
    env: str | None

    class Config:
        env_prefix = "sentry_"


class BotConfig(EnvBaseSettings):
    api_id: str = ""
    api_hash: str = ""
    token: str = ""

    class Config:
        env_prefix = "bot_"


class ParseConfig(EnvBaseSettings):
    api_id: str = ""
    api_hash: str = ""
    string_session: str = ""
    news_channel: str = ""
    key_word: str = ""

    class Config:
        env_prefix = "parse_"


class OpenWeatherConfig(EnvBaseSettings):
    api_key: str = ""

    class Config:
        env_prefix = "openweather_"


class RateConfig(EnvBaseSettings):
    api_url: str = ""

    class Config:
        env_prefix = "rate_"


class Settings(BaseSettings):
    base_dir: Path = BASE_DIR
    app: AppSettings = AppSettings(name="mailing_bot")
    database: PostgresConfig = PostgresConfig()
    bot: BotConfig = BotConfig()
    sentry: SentryConfig = SentryConfig()
    logger: LoggingSettings = LoggingSettings()
    open_weather: OpenWeatherConfig = OpenWeatherConfig()
    broker: BrokerConfig = BrokerConfig()
    parse: ParseConfig = ParseConfig()
    rate: RateConfig = RateConfig()
    admin_tg_id: int = 1111111
