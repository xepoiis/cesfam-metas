from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone

from database import engine, Base, SessionLocal
import models, schemas

SECRET_KEY = "clave_super_secreta_cesfam_2026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API CESFAM Santa Rosa",
    description="Motor de cálculo IAAPS y Metas Sanitarias"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def estado_servidor():
    return {"estado": "En línea", "mensaje": "¡Motor de Cálculo CESFAM operativo!"}

@app.post("/usuarios/")
def registrar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(models.Usuario).filter(models.Usuario.rut == usuario.rut).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El RUT ya está registrado")
    
    password_bytes = usuario.password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt).decode('utf-8') 
    
    nuevo_usuario = models.Usuario(
        rut=usuario.rut,
        nombre=usuario.nombre,
        rol=usuario.rol,
        password_hash=hashed_password
    )
    
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return {"mensaje": "Usuario creado exitosamente", "rut": nuevo_usuario.rut, "rol": nuevo_usuario.rol}

@app.post("/login/")
def iniciar_sesion(credenciales: schemas.UsuarioLogin, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.rut == credenciales.rut).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="RUT o contraseña incorrectos")
    
    password_ingresada_bytes = credenciales.password.encode('utf-8')
    password_guardada_bytes = usuario.password_hash.encode('utf-8')
    
    if not bcrypt.checkpw(password_ingresada_bytes, password_guardada_bytes):
        raise HTTPException(status_code=401, detail="RUT o contraseña incorrectos")
        
    expiracion = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    datos_token = {
        "sub": usuario.rut,     
        "rol": usuario.rol,     
        "exp": expiracion       
    }
    
    token_jwt = jwt.encode(datos_token, SECRET_KEY, algorithm=ALGORITHM)
    
    return {
        "access_token": token_jwt, 
        "token_type": "bearer",
        "rol": usuario.rol
    }