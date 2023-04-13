import json
from urllib import request

from app.api.api_v1.api import api_router
from app.core.config import settings
from fastapi import FastAPI

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="{0}/openapi.json".format(settings.API_V1_STR),
)


@app.get("/random", tags=["misc"])
async def random():
    """Route to random number."""
    from random import random  # noqa: WPS433, WPS442

    return {"random_number": random()}  # noqa: S311


@app.get("/", tags=["misc"])
async def hello_world():
    """Route to hello world."""
    return {"msg": "See /docs"}


@app.get("/xkcd", tags=["xkcd"])
async def xkcd_current():
    """Route to xkcd."""
    ff = request.urlopen("http://xkcd.com/info.0.json")  # noqa: S310
    resp = ff.read().decode("utf-8")
    return json.loads(resp)


@app.get("/xkcd/{comic_id}", tags=["xkcd"])
async def xkcd_comic(comic_id: int):
    """Route to xkcd_comic."""
    ff = request.urlopen("http://xkcd.com/info.0.json")  # noqa: S310
    resp = ff.read().decode("utf-8")
    return json.loads(resp)


app.include_router(api_router, prefix=settings.API_V1_STR)
