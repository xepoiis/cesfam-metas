import jwt
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from database import get_db
from models import Usuario

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])

SECRET_KEY = "Firma_Secreta_CESFAM_2026"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login")
def login(rut: str, password: str, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.rut == rut).first()
    
    if not usuario or not pwd_context.verify(password, usuario.password_hash):
        raise HTTPException(status_code=401, detail="RUT o contraseña incorrectos")
    
    if not usuario.activo:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
        
    payload = {
        "sub": usuario.rut,
        "nombre": usuario.nombre,
        "id_rol": usuario.id_rol,
        "exp": datetime.now(timezone.utc) + timedelta(hours=2) 
    }
    
    token_real = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": token_real,
        "token_type": "bearer",
        "id_rol": usuario.id_rol
    }

import random
import string
from pydantic import BaseModel

# Esquema para recibir los datos de la nueva contraseña
class ResetPasswordRequest(BaseModel):
    rut: str
    codigo: str
    nueva_password: str

@router.post("/recuperar-password")
def solicitar_codigo(rut: str, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.rut == rut).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Generar código de 6 dígitos
    codigo = ''.join(random.choices(string.digits, k=6))
    usuario.codigo_recuperacion = codigo
    db.commit()
    
    # Simular envío de correo en la terminal de Uvicorn
    print(f"\n{'='*50}\n📧 SIMULADOR EMAIL CESFAM\nPara: {usuario.email}\nAsunto: Código de Recuperación\nTu código de seguridad es: {codigo}\n{'='*50}\n")
    
    return {"mensaje": "Código enviado al correo asociado"}

@router.post("/reset-password")
def reset_password(datos: ResetPasswordRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.rut == datos.rut).first()
    
    if not usuario or usuario.codigo_recuperacion != datos.codigo:
        raise HTTPException(status_code=400, detail="Código inválido o expirado")
    
    # Hashear nueva contraseña y limpiar el código
    usuario.password_hash = pwd_context.hash(datos.nueva_password)
    usuario.codigo_recuperacion = None
    db.commit()
    
    return {"mensaje": "Contraseña actualizada con éxito"}