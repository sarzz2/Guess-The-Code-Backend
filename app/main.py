import os
from fastapi import FastAPI

from .routers import generate_code_block
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# from starlette.middleware.sessions import SessionMiddleware

from .utils.log_stream import LogStreamHandler

# from .utils.databse import DataBase
from dotenv import load_dotenv
import logging

logger = logging.getLogger("root")
logger.addHandler(LogStreamHandler())
logger.setLevel(logging.DEBUG)

load_dotenv()
TOKEN = os.getenv("TOKEN")
URI = os.getenv("URI")

tags_metadata = []
app = FastAPI(openapi_tags=tags_metadata)

# Middlewares
app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["127.0.0.1", ""]
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# app.add_middleware(SessionMiddleware, secret_key="!secret")

# Router apps setup
app.include_router(generate_code_block.router, prefix="/api")

# database setup and models registration
# @app.on_event("startup")
# async def startup():
#     database_instance = DataBase(
#         user="sarzz", password="password", database="taproduction", host="localhost"
#     )
#     await database_instance.connect()
#     app.state.db = database_instance
#
#
# @app.on_event("shutdown")
# async def shutdown_event():
#     if not app.state.db:
#         await app.state.db.close()
