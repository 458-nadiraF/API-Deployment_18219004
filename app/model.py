# app/model.py

from pydantic import BaseModel, Field


class UserLoginSchema(BaseModel):
    username: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "username": "nadiraFM",
                "password": "i2c"
            }
        }