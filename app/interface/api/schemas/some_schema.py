from pydantic import BaseModel


class SomeSchema(BaseModel):
    a: int
    b: str


class SomeSchemaIn(SomeSchema):
    pass


class SomeSchemaOut(SomeSchema):
    pass
