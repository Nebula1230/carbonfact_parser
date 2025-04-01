from pydantic import BaseModel, Field
from typing import List, Optional

class Material(BaseModel):
    fabric_type: Optional[str] = None
    name: str
    percentage: int

class ConstructionElement(BaseModel):
    name: str
    colors: List[str] = Field(default_factory=list)
    materials: List[Material]
    weight: str

class Garment(BaseModel):
    code: str
    category: str
    construction: List[ConstructionElement]