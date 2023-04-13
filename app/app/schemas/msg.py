from pydantic import BaseModel


class Msg(BaseModel):
    """Msg class."""

    msg: str
