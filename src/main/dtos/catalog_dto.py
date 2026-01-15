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
    perfume: str
    ml: int
    preco: float
    tipo: str
    tags: List[str]
    imagem_url: str | None


class CatalogResponseDTO(BaseModel):
    sucess: bool
    message: str | List[CatalogGetPerfumeResponseDTO] | List[None]
