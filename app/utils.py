import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

import emails  # type: ignore [import]
from emails.template import JinjaTemplate  # type: ignore [import]
from jose import jwt
from jose.exceptions import JWTError

from app.core.config import settings

KEMAIL = "email"


def ensure_int(valor: Optional[int], emsg: str) -> int:
    """Return the int value if not None.

    Args:
        valor (int): Value to ensure
        emsg (str): Error message

    Raises:
        ValueError: if valor is None

    Returns:
        int: Valor if not None
    """
    if valor is None:
        raise ValueError(emsg)
    return valor


def ensure_str(valor: Optional[str], emsg: str) -> str:
    """Return the str value if not None.

    Args:
        valor (str): Value to ensure
        emsg (str): Error message

    Raises:
        ValueError: if valor is None

    Returns:
        str: Valor if not None
    """
    if valor is None:
        raise ValueError(emsg)
    return valor


def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Optional[Dict[str, Any]] = None,
) -> None:
    """Send an email."""
    assert (  # noqa: S101
        settings.EMAILS_ENABLED
    ), "no provided configuration for email variables"
    if environment is None:
        environment = {}
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    logging.info("send email result: {0}".format(response))


def send_test_email(email_to: str) -> None:
    """Send test email."""
    project_name = settings.PROJECT_NAME
    subject = "{0} - Test email".format(project_name)
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "test_email.html") as ff:
        template_str = ff.read()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={"project_name": settings.PROJECT_NAME, KEMAIL: email_to},
    )


def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    """Send a reset password email."""
    subject = "{0} - Password recovery for user {1}".format(
        settings.PROJECT_NAME,
        email,
    )
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "reset_password.html") as ff:
        template_str = ff.read()
    server_host = settings.SERVER_HOST
    link = "{0}/reset-password?token={1}".format(server_host, token)
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            KEMAIL: email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )


def send_new_account_email(email_to: str, username: str, password: str) -> None:
    """Send a new account email."""
    project_name = settings.PROJECT_NAME
    subject = "{0} - New account for user {1}".format(project_name, username)
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "new_account.html") as ff:
        template_str = ff.read()
    link = settings.SERVER_HOST
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "password": password,
            KEMAIL: email_to,
            "link": link,
        },
    )


def generate_password_reset_token(email: str) -> str:
    """Generate a new password reset token."""
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    return jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        settings.SECRET_KEY,
        algorithm="HS256",
    )


def verify_password_reset_token(token: str) -> Optional[str]:
    """Verify password reset token."""
    try:
        decoded_token = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"],
        )
        return decoded_token[KEMAIL]
    except JWTError:
        return None
