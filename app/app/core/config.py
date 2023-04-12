import secrets
from os import getenv
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, validator

load_dotenv()  # take environment variables from .env.


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_NAME: Optional[str] = getenv("SERVER_NAME", "example.com")
    SERVER_HOST: Optional[AnyHttpUrl] = AnyHttpUrl(
        getenv("SERVER_HOST", "http://example.com"),
    )

    PROJECT_NAME: str = "banned-fastapi"

    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "/app/app/email-template/build"
    EMAILS_ENABLED: bool = False

    @validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if not v:
            return values["PROJECT_NAME"]
        return v

    @validator("EMAILS_ENABLED", pre=True, check_fields=False)
    def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
        )

    EMAIL_TEST_USER: EmailStr = EmailStr("test@example.com")
    FIRST_SUPERUSER: EmailStr = EmailStr(
        getenv("FIRST_SUPERUSER", "admin@example.com"),
    )
    FIRST_SUPERUSER_PASSWORD: str = getenv("FIRST_SUPERUSER_PASSWORD", "password")
    USERS_OPEN_REGISTRATION: bool = False

    class Config:
        case_sensitive = True


settings = Settings()
