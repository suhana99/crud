# schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class ItemBase(BaseModel):
    name: str
    age: Optional[int] = None
    email: Optional[EmailStr] = None

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[EmailStr] = None

class ItemOut(ItemBase):
    id: int

    class Config:
        orm_mode = True
