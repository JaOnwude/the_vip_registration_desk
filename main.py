from typing import Annotated, Any
from fastapi import FastAPI, Header, Body, Cookie, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()


class BaseHeaderModel(BaseModel):
    x_union_pass: str = Field(alias="X-Union-Pass")
    x_client_version: str = Field(default="1.0", alias="X-Client-Version")


class StaffOut(BaseModel):
    username: str = Field(min_length=3, description="Your username goes here.")
    full_name: str | None = Field(default=None, description="Your full name goes here.")
    station: str = Field(description="Your station goes here.")


class StaffIn(StaffOut):
    password: str = Field(min_length=8, description="Enter your password here.")

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "JaOnwude",
                "full_name": "Onwude James Uchenna",
                "password": "James@123456",
                "station": "Terminal A1 - VIP",
            }
        }
    }


class CookiesModel(BaseModel):
    session_id: str
    language: str = "en"


class GreetingResponse(BaseModel):
    greeting: str
    session_id: str


@app.post("/staff", response_model=StaffOut, status_code=status.HTTP_201_CREATED)
async def register_staff(
    headers: Annotated[BaseHeaderModel, Header()], 
    staff: Annotated[StaffIn, Body()]
) -> Any:
    if headers.x_union_pass != "UNION-2026-VIP":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong pass.",
        )

    return staff


@app.get("/desk/greeting", response_model=GreetingResponse)
async def greet_visitor(cookies: Annotated[CookiesModel, Cookie()]) -> Any:
    if cookies.language == "en":
        message = "Welcome back!"
    elif cookies.language == "pidgin":
        message = "How far, you don come again!"
    else:
        message = "Welcome!"

    return {
        "greeting": message,
        "session_id": cookies.session_id,
    }