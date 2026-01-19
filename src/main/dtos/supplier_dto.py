from pydantic import BaseModel, EmailStr
from typing import List, Optional


class SupplierGetRequestDTO(BaseModel):
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
    message: str | List[SupplierGetResponseDTO] | List[None]
