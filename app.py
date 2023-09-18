import uvicorn
from fastapi import FastAPI

from config import settings
from database import init_db
from utils.utils import include_api_routes, import_db_models

app = FastAPI()
include_api_routes(app)


@app.on_event('startup')
async def startup_event():
    import_db_models()
    # await init_db()
    return

if __name__ == '__main__':
    uvicorn.run(
        'app:app',
        host=settings.SRV_HOST,
        port=settings.SRV_PORT,
        log_level='debug',
        access_log=True,
    )
