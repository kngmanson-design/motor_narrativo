from typing import Dict, List, Union

from pydantic import BaseModel, Field


class PeticionHistoria(BaseModel):
    id_partida: Union[str, int]
    nodo_actual: str = Field(..., examples=["inicio"])
    decision_usuario: str = Field(..., examples=["A"])
    inventario: List[str] = Field(default_factory=list, examples=[["llave_de_cobre"]])


class RespuestaHistoria(BaseModel):
    id_partida: Union[str, int]
    nodo_actual: str
    texto: str
    opciones: Dict[str, str]
    inventario: List[str]
    es_final: bool
