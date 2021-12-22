from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.settings import get_settings
from app.database import create_db_and_tables
from app.routers import drones, medications

settings = get_settings()
app = FastAPI(
    debug=settings.debug,
    title=settings.project_name,
    description="Musala Soft Practical Task: **Drones API**",
    version="0.1",
    contact={
        "name": "Oscar L. Garcell",
        "url": "https://github.com/codeshard/drones-api",
    },
    license_info={
        "name": "MIT",
        "url": "https://mit-license.org/",
    },
)

origins = [
    "http://127.0.0.1",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await create_db_and_tables()


app.include_router(drones.router)
app.include_router(medications.router)
