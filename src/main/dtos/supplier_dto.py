from pydantic import BaseModel, EmailStr
from typing import List, Optional


class SupplierCreateRequestDTO(BaseModel):
    razao: str
    email: Optional[EmailStr] = None
    cnpj: Optional[str] = None
    numero_tel: Optional[str] = None
    cep: Optional[str] = None
    rua: Optional[str] = None
    numero: Optional[int] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None
    pais: Optional[str] = None


class SupplierGetResponseDTO(BaseModel):
    id: int
    razao: str
    email: Optional[EmailStr]
    cnpj: Optional[str]
    numero_tel: Optional[str]
    cep: Optional[str]
    rua: Optional[str]
    numero: Optional[int]
    cidade: Optional[str]
    uf: Optional[str]
    pais: Optional[str]


class SupplierResponseDTO(BaseModel):
    sucess: bool
    message: str | dict | List[SupplierGetResponseDTO] | List[None]


class SupplierUpdateRequestDTO(BaseModel):
    razao: Optional[str] = None
    email: Optional[EmailStr] = None
    cnpj: Optional[str] = None
    numero_tel: Optional[str] = None
    cep: Optional[str] = None
    rua: Optional[str] = None
    numero: Optional[int] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None
    pais: Optional[str] = None
