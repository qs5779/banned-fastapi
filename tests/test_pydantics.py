from pydantic import AnyHttpUrl, BaseModel, EmailStr
from pydantic.tools import parse_obj_as

TEMAIL = "foo@example.com"
THTTP = "http://wtf.example.org"
THTTPS = "https://wtf.example.org"


def test_email_str():
    """Function test_email_str."""

    class Model(BaseModel):  # noqa: WPS431
        email: EmailStr

    assert Model(email=EmailStr(TEMAIL)).email == TEMAIL
    assert Model(email=TEMAIL).email == TEMAIL


def test_any_http_url():
    """Function test_any_http_url."""

    class Model(BaseModel):  # noqa: WPS431
        url: AnyHttpUrl

    assert Model(url=parse_obj_as(AnyHttpUrl, THTTP)).url == THTTP
