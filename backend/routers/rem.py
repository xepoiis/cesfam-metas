from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from models import TablaRemMensual, LogAuditoria 
from services.motor_calculo import procesar_planilla_rem

router = APIRouter(prefix="/api/rem", tags=["Carga REM"])

@router.post("/carga", status_code=status.HTTP_201_CREATED)
async def cargar_archivo(
    # Agregamos Form(...) para recibir datos de texto junto con el archivo
    celda_pob: str = Form(...), 
    celda_comp: str = Form(...),
    archivo: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    # Pasamos las celdas dinámicas al motor
    datos = await procesar_planilla_rem(archivo, celda_pob, celda_comp)
    
    try:
        # Guardamos registro indicando qué celda se usó como referencia principal
        nuevo_registro = TablaRemMensual(
            mes="Octubre",
            anio=2026,
            hoja_excel="REM_General",
            celda_referencia=celda_comp, # Dinámico
            valor_obtenido=datos.get("pacientes_compensados", 0),
            id_usuario_carga=1 
        )
        db.add(nuevo_registro)
        
        log = LogAuditoria(
            id_usuario=1,
            accion="CARGA_REM_IAAPS",
            payload_json={
                "archivo": archivo.filename,
                "celdas_parametrizadas": {"poblacion": celda_pob, "compensados": celda_comp},
                "resultados": datos,
                "timestamp": datetime.now().isoformat()
            }
        )
        db.add(log)
        db.commit()
        
        return {"mensaje": "Carga y cálculo exitoso", "data": datos}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error de BD: {str(e)}")