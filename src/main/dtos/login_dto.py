from pydantic import BaseModel, EmailStr


class LoginResponseDTO(BaseModel):
    message: str
    sucess: bool
    access_token: str = None


class LoginRequestDTO(BaseModel):
    email: EmailStr = None
    password: str


class NewLoginRequestDTO(BaseModel):
    email: EmailStr
    password: str
    user: str
    nome: str
    cpf: str
    sexo: str = None
    numero_tel: int = None
    cep: str = None
    rua: str = None
    numero: int = None
    cidade: str = None
    uf: str = None
