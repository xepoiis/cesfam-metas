import io
import openpyxl
from fastapi import UploadFile, HTTPException

# Ahora la función exige que le digamos qué celdas buscar
async def procesar_planilla_rem(archivo: UploadFile, celda_pob: str, celda_comp: str):
    if not archivo.filename.endswith(('.xlsx', '.xlsm')):
        raise HTTPException(status_code=400, detail="Debe ser Excel (.xlsx o .xlsm)")

    try:
        contenido = await archivo.read()
        workbook = openpyxl.load_workbook(io.BytesIO(contenido), data_only=True)
        hoja = workbook.active 
        
        # Usamos las variables dinámicas en lugar de 'J25' y 'M40'
        resultados = {
            "poblacion_diabetica": hoja[celda_pob].value or 0,
            "pacientes_compensados": hoja[celda_comp].value or 0,
        }
        
        # Lógica IAAPS
        if resultados["poblacion_diabetica"] > 0:
            cumplimiento = (resultados["pacientes_compensados"] / resultados["poblacion_diabetica"]) * 100
        else:
            cumplimiento = 0
            
        resultados["cumplimiento_porcentual"] = round(cumplimiento, 2)
        return resultados

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando Excel: {str(e)}")