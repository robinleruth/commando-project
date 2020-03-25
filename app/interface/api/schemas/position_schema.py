from pydantic import BaseModel
from datetime import date


class PositionSchema(BaseModel):
    as_of_date: date
    side: str
    qty: int
    pos_value: float
    take_profit: float
    stop_loss: float
    initial_pos_value: float
