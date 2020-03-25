from fastapi import FastAPI
from fastapi import Header
from fastapi import HTTPException
from fastapi import Depends
from fastapi.middleware.cors import CORSMiddleware

from app.infrastructure.config import app_config


api = FastAPI(title='Commando API',
              description='Portfolio management',
              version='0.1')

async def get_token_header(x_token: str = Header(...)):
    if x_token != app_config.API_TOKEN:
        raise HTTPException(status_code=400, detail="X-Token header invalid")


from .controllers import some_controller, backtester_controller
# api.include_router(some_controller.router,
#                    prefix='/api/v1/some_controller',
#                    tags=['some_controller'],
#                    dependencies=[Depends(get_token_header)])
api.include_router(backtester_controller.router,
                   prefix='/api/v1/backtester_controller',
                   tags=['backtester_controller'])


api.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
