import logfire
import os
import logging.config
from app.core.config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import user as user_router
from app.db.database import engine

# Configure logfire and logging as early as possible
logfire.configure(token=settings.LOGFIRE_WRITE_TOKEN, environment=settings.LOGFIRE_ENVIRONMENT)

LOGGING_CONFIG_FILE = "logging.conf"
if os.path.exists(LOGGING_CONFIG_FILE):
    logging.config.fileConfig(LOGGING_CONFIG_FILE, disable_existing_loggers=False)
else:
    logging.basicConfig(level=logging.INFO)
    logging.getLogger().warning(
        f"Logging config file '{LOGGING_CONFIG_FILE}' not found. Using basicConfig."
    )

logfire.instrument_sqlalchemy(engine)
logfire.instrument_psycopg()

app = FastAPI()

logfire.instrument_fastapi(app, capture_headers=True)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.API_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the user CRUD API router
app.include_router(user_router.router)


@app.get("/")
def read_root():
    # You can access settings anywhere in your app
    return {"Welcome to the API": "This is a FastAPI application with CORS enabled."}
