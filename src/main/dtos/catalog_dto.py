from pydantic import BaseModel
from typing import List


class CatalogNewPerfumeRequestDTO(BaseModel):
    perfume: str
    ml: int
    preco: float
    tipo: str
    tags: List[str]
    imagem_url: str = None


class CatalogGetPerfumeResponseDTO(BaseModel):
    id: int
    perfume: str
    ml: int
    preco: float
    tipo: str
    tags: List[str]
    imagem_url: str | None


class CatalogResponseDTO(BaseModel):
    sucess: bool
    message: str | dict | List[CatalogGetPerfumeResponseDTO] | List[None]


class CatalogUpdatePerfumeRequestDTO(BaseModel):
    perfume: str = None
    ml: int = None
    preco: float = None
    tipo: str = None
    tags: List[str] = None
