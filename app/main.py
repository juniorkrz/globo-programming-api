__version__ = "1.0.0"
__author__ = "Antônio Roberto Júnior"


from fastapi import FastAPI

from .tokens import scraping_ant_tokens
from app.globo import GloboProgramming


app = FastAPI()
prog = GloboProgramming(scraping_ant_tokens)


@app.get("/")
async def root():
    return {
                "author": __author__,
                "version": __version__,
                "message": "Globo Programming API Online!",
                "git": "https://github.com/juniorkrz/globo-programming-api"
            }


@app.get("/channels")
async def channels():
    return {
            "status": True,
            "result": prog.load_channels()
        }


@app.get("/channelPrograms/{name}")
async def channel_programs(name):
    result = prog.load_channel_programs(name.lower())
    return {
            "status": result.get("status"),
            "message": result.get("message"),
            "result": result.get("result")
        }