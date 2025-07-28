"""Get .env configurations for safe use elsewhere."""

import pathlib
from pydantic_settings import BaseSettings, SettingsConfigDict


class DotEnvSettings(BaseSettings):
    """Extract settings."""

    model_config = SettingsConfigDict(
        env_file=pathlib.Path(__file__).parent.absolute() / ".env"
    )
    HOST: str = "0.0.0.0"
    OPENAI_API_KEY: str = ""
    HF_TOKEN: str = ""


dot_env_settings = DotEnvSettings()

if __name__ == "__main__":
    print("""
    To access this from another file:
    1. Rename .env.example to .env and enter credentials.

    2. Then you can import and access the information like this:
    >>> from dotenv_config import dot_env_settings
    >>> token = dot_env_settings.HF_TOKEN
    """)