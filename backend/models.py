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
    rut = Column(String(12), unique=True, index=True, nullable=False) # Ej: 12345678-9
    nombre = Column(String(100), nullable=False)
    rol = Column(String(50), nullable=False) # Roles: Director, Subdirector, Gestor
    password_hash = Column(String(255), nullable=False) # Nunca guardaremos la clave en texto plano