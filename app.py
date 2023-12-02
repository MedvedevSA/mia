from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from config import settings
from database import init_db
from utils.utils import include_routes, import_db_models

app = FastAPI()

include_routes(app, Path('./api'), prefix='/api')
include_routes(app, Path('./pages'))
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def redirect_typer():
    return RedirectResponse("/customers")


@app.on_event('startup')
async def startup_event():
    import_db_models()
    await init_db()

if __name__ == '__main__':
    uvicorn.run(
        'app:app',
        host=settings.SRV_HOST,
        port=settings.SRV_PORT,
        log_level='debug',
        access_log=True,
    )
