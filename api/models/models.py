from pydantic import BaseModel, Field
from typing import Optional

class Address(BaseModel):
    city: str = Field(..., min_length=1)
    country: str = Field(..., min_length=1)

class AddressUpdate(BaseModel):
    city: Optional[str] = Field(None, min_length=1)
    country: Optional[str] = Field(None, min_length=1)

class StudentBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    age: int = Field(..., ge=1, le=100)
    address: Address

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=50)
    age: Optional[int] = Field(None, ge=1, le=100)
    address: Optional[AddressUpdate]

class StudentResponse(BaseModel):
    id: str
    name: str
    age: int
    address: Address
