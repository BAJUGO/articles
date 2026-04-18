from pydantic import BaseModel


class AccessTokenData(BaseModel):
    sub: str
    name: str
    role: str
    id: int