from pydantic import BaseModel


class Session(BaseModel):
    token: str
    state: str
