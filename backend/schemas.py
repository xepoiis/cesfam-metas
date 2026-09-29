from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    rut: str
    nombre: str
    rol: str
    password: str

class UsuarioLogin(BaseModel):
    rut: str
    password: str