import io
import openpyxl
from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone

from database import engine, Base, SessionLocal
import models, schemas

SECRET_KEY = "cesfam2026" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120 

security = HTTPBearer()

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

def verificar_token(credenciales: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credenciales.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="El token expiró. Inicia sesión nuevamente.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido o corrupto.")

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
    
    nuevo_usuario = models.Usuario(rut=usuario.rut, nombre=usuario.nombre, rol=usuario.rol, password_hash=hashed_password)
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return {"mensaje": "Usuario creado", "rut": nuevo_usuario.rut, "rol": nuevo_usuario.rol}

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
    datos_token = {"sub": usuario.rut, "rol": usuario.rol, "exp": expiracion}
    token_jwt = jwt.encode(datos_token, SECRET_KEY, algorithm=ALGORITHM)
    
    return {"access_token": token_jwt, "token_type": "bearer", "rol": usuario.rol}

@app.post("/piv/")
def registrar_piv(datos: schemas.PIVCreate, db: Session = Depends(get_db), usuario_actual: dict = Depends(verificar_token)):
    if usuario_actual.get("rol") not in ["Gestor", "Director"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para ingresar datos PIV")
    
    nuevo_registro = models.TablaPIV(mes=datos.mes, anio=datos.anio, parametro=datos.parametro, valor_obtenido=datos.valor_obtenido)
    db.add(nuevo_registro)
    db.commit()
    db.refresh(nuevo_registro)
    return {"mensaje": "Dato PIV ingresado correctamente", "parametro": nuevo_registro.parametro, "registrado_por": usuario_actual["sub"]}

@app.post("/extrasistema/")
def registrar_extrasistema(datos: schemas.ExtrasistemaCreate, db: Session = Depends(get_db), usuario_actual: dict = Depends(verificar_token)):
    if usuario_actual.get("rol") not in ["Gestor", "Director"]:
        raise HTTPException(status_code=403, detail="No tienes permisos")
    
    nuevo_registro = models.TablaExtrasistema(mes=datos.mes, anio=datos.anio, meta_asociada=datos.meta_asociada, cantidad_atenciones=datos.cantidad_atenciones)
    db.add(nuevo_registro)
    db.commit()
    db.refresh(nuevo_registro)
    return {"mensaje": "Dato de Extrasistema ingresado", "meta": nuevo_registro.meta_asociada}

@app.post("/continuidad/")
def registrar_continuidad(datos: schemas.ContinuidadCreate, db: Session = Depends(get_db), usuario_actual: dict = Depends(verificar_token)):
    if usuario_actual.get("rol") not in ["Gestor", "Director"]:
        raise HTTPException(status_code=403, detail="No tienes permisos")
    
    nuevo_registro = models.TablaContinuidad(mes=datos.mes, anio=datos.anio, porcentaje_obtenido=datos.porcentaje_obtenido)
    db.add(nuevo_registro)
    db.commit()
    db.refresh(nuevo_registro)
    return {"mensaje": "Porcentaje de Continuidad ingresado", "porcentaje": nuevo_registro.porcentaje_obtenido}

@app.post("/cargar-rem/")
async def procesar_archivo_rem(
    mes: str = Form(...), 
    anio: int = Form(...), 
    hoja_excel: str = Form(...),
    celdas_extraer: str = Form(...),
    archivo: UploadFile = File(...), 
    db: Session = Depends(get_db), 
    usuario_actual: dict = Depends(verificar_token)
):
    if usuario_actual.get("rol") not in ["Gestor", "Director"]:
        raise HTTPException(status_code=403, detail="No tienes permisos para cargar el REM")
    
    if not archivo.filename.endswith(('.xls', '.xlsx', '.xlsm')):
        raise HTTPException(status_code=400, detail="El archivo debe ser un Excel")
    
    contenido_archivo = await archivo.read()
    
    try:
        wb = openpyxl.load_workbook(io.BytesIO(contenido_archivo), data_only=True)
        
        if hoja_excel not in wb.sheetnames:
            raise HTTPException(status_code=400, detail=f"El archivo no tiene la hoja '{hoja_excel}'")
        
        hoja = wb[hoja_excel]
        
        lista_celdas = [celda.strip() for celda in celdas_extraer.split(',')]
        resultados = []
        
        for celda in lista_celdas:
            valor_celda = hoja[celda].value
            valor_final = int(valor_celda) if valor_celda is not None else 0
            
            nuevo_dato = models.TablaREM(
                mes=mes,
                anio=anio,
                hoja_excel=hoja_excel,
                celda_referencia=celda,
                valor_obtenido=valor_final
            )
            db.add(nuevo_dato)
            resultados.append({"celda": celda, "valor": valor_final})
            
        db.commit()

        return {
            "mensaje": "Archivo REM procesado y datos extraídos",
            "archivo": archivo.filename,
            "hoja_procesada": hoja_excel,
            "datos_guardados": resultados
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el Excel: {str(e)}")