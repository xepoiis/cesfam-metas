from sqlalchemy import Column, Integer, String, Numeric
from database import Base

class TablaPIV(Base):
    __tablename__ = "trn_piv_mensual"

    id_piv = Column(Integer, primary_key=True, index=True)
    mes = Column(String(20), nullable=False) 
    anio = Column(Integer, nullable=False)   
    parametro = Column(String(100), nullable=False) 
    valor_obtenido = Column(Numeric(14, 4), nullable=False) 

class Usuario(Base):
    __tablename__ = "trn_usuario"
    
    id_usuario = Column(Integer, primary_key=True, index=True)
    rut = Column(String(12), unique=True, index=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    rol = Column(String(50), nullable=False)
    password_hash = Column(String(255), nullable=False)

class TablaExtrasistema(Base):
    __tablename__ = "trn_extrasistema"
    
    id_extra = Column(Integer, primary_key=True, index=True)
    mes = Column(String(20), nullable=False)
    anio = Column(Integer, nullable=False)
    meta_asociada = Column(String(100), nullable=False)
    cantidad_atenciones = Column(Integer, nullable=False)

class TablaContinuidad(Base):
    __tablename__ = "trn_continuidad_iaaps"
    
    id_cont = Column(Integer, primary_key=True, index=True)
    mes = Column(String(20), nullable=False)
    anio = Column(Integer, nullable=False)
    porcentaje_obtenido = Column(Numeric(5, 2), nullable=False)