import asyncio
import os
import random
from fastapi import APIRouter, Request
import requests
from fastapi.responses import JSONResponse
from fastapi.websockets import WebSocket
from dotenv import load_dotenv

router = APIRouter()
load_dotenv()
TOKEN = os.getenv("TOKEN")


@router.get("/code-block", tags=[""])
async def code_block(request: Request):
    page = random.Random().randint(1, 30)
    code = requests.get(f"https://api.github.com/gists/public?page={page}", auth=("sarzz2", TOKEN))
    result = code.json()
    r = random.Random().randint(0, len(result))
    raw_url = str(list((result[r]["files"]).values())[0]["raw_url"])
    language = str(list((result[r]["files"]).values())[0]["language"])
    block = requests.get(raw_url, auth=("sarzz2", TOKEN))
    # TODO implement fuzzy matching
    all_languages = [
        "JavaScript",
        "Python",
        "Go",
        "Java",
        "C++",
        "TypeScript",
        "C",
        "PHP",
        "C#",
        "Shell",
        "Ruby",
        "Swift",
        "Rust",
        "Kotlin",
        "Dart",
        "Vim Script",
        "Scala",
        "Lua",
        "Emacs Lisp",
        "Powershell",
        "CoffeeScript",
        "Elixir",
        "Haskell",
        "Groovy",
        "R",
        "Erlang",
        "Pascal",
        "MATLAB",
        "Assembly",
        "Nix",
        "Common Lisp",
        "Julia",
        "F#",
        "TSQL",
        "Nim",
        "Fortran",
        "Visual Basic",
        "CSV",
        "Bash",
    ]
    xyz = random.sample(all_languages, 4)
    if language not in xyz:
        xyz[random.randint(1, 3)] = language
    return JSONResponse(
        content={"block": str(block.text[0:450]), "language": xyz, "answer": language}
    )


@router.websocket("/ws")
async def websocket(ws: WebSocket):
    await ws.accept()
    count = 10
    while True:
        await ws.send_text(str(count))
        count -= 1
        await asyncio.sleep(1)
        if count == -1:
            break
