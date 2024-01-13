from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    company_id: int


class User(BaseModel):
    id: int
    name: str
    email: str
    role: str = "USER"
    company_id: int

    class Config():
        orm_mode = True
