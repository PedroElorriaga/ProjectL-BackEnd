from pydantic import BaseModel, EmailStr


class LoginResponseDTO(BaseModel):
    message: str
    sucess: bool
    access_token: str = None


class LoginRequestDTO(BaseModel):
    email: EmailStr = None
    senha: str
