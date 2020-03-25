from fastapi import APIRouter
from fastapi import BackgroundTasks
from typing import List

from app.interface.api.schemas.some_schema import SomeSchemaOut
from app.interface.api.schemas.some_schema import SomeSchemaIn


router = APIRouter()


@router.post('/', response_model=List[SomeSchemaOut])
async def aaa(inst: SomeSchemaIn):
    return [inst for _ in range(4)]


@router.get('/write_as_bg_task')
async def write_as_bg_task(bg_tasks: BackgroundTasks):
    bg_tasks.add_task(write_in_file, 'a message from controller')
    return SomeSchemaOut(a=1, b='ok')

def write_in_file(message: str):
    with open('test.txt', 'w') as f:
        f.write(f'{message} is written in a background task')
