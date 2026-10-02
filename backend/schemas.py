from pydantic import BaseModel
from enum import Enum

class RolUsuario(str, Enum):
    directora = "Directora"
    subdireccion = "Subdireccion"
    gestor = "GDI"
    jefe = "Jefe de Programa"

class UsuarioCreate(BaseModel):
    rut: str
    nombre: str
    password: str
    rol: RolUsuario

class UsuarioLogin(BaseModel):
    rut: str
    password: str

class PIVCreate(BaseModel):
    mes: str
    anio: int
    parametro: str
    valor_obtenido: float

class ExtrasistemaCreate(BaseModel):
    mes: str
    anio: int
    meta_asociada: str
    cantidad_atenciones: int

class ContinuidadCreate(BaseModel):
    mes: str
    anio: int
    porcentaje_obtenido: float