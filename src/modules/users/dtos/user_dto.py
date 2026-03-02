from pydantic import BaseModel, EmailStr


class UserResponseDTO(BaseModel):
    message: str
    sucess: bool
    access_token: str = None


class UserCreateRequestDTO(BaseModel):
    senha: str
    email: EmailStr
    nome: str
    sexo: str = None
    cpf: str
    numero_tel: str = None
    cep: str = None
    rua: str = None
    numero_residencia: int = None
    cidade: str = None
    uf: str = None
