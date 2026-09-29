from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    rut: str
    nombre: str
    rol: str
    password: str

class UsuarioLogin(BaseModel):
    rut: str
    password: str

class PIVCreate(BaseModel):
    mes: str
    anio: int
    parametro: str
    valor_obtenido: float