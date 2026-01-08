from pydantic import BaseModel, EmailStr


class LoginResponseDTO(BaseModel):
    message: str
    sucess: bool


class LoginRequestDTO(BaseModel):
    email: EmailStr
    password: str
