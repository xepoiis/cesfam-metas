from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base

class SysRole(Base):
    __tablename__ = "sys_roles"
    
    id_rol = Column(Integer, primary_key=True, index=True)
    nombre_rol = Column(String(50), unique=True, nullable=False)

class Usuario(Base):
    __tablename__ = "trn_usuario"
    
    id_usuario = Column(Integer, primary_key=True, index=True)
    rut = Column(String(12), unique=True, index=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), nullable=True)
    password_hash = Column(String(255), nullable=False)
    codigo_recuperacion = Column(String(6), nullable=True)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    ultimo_acceso = Column(DateTime, nullable=True)
    id_rol = Column(Integer, ForeignKey("sys_roles.id_rol"))


class LogAuditoria(Base):
    __tablename__ = "log_auditoria"
    
    id_log = Column(Integer, primary_key=True, index=True)
    fecha_hora = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    id_usuario = Column(Integer, ForeignKey("trn_usuario.id_usuario"))
    accion = Column(String(50), nullable=False)
    payload_json = Column(JSONB, nullable=False)


class TablaRemMensual(Base):
    __tablename__ = "trn_rem_mensual"
    
    id_rem = Column(Integer, primary_key=True, index=True)
    mes = Column(String(20), nullable=False)
    anio = Column(Integer, nullable=False)
    hoja_excel = Column(String(50))
    celda_referencia = Column(String(50))
    valor_obtenido = Column(Integer)

    id_usuario_carga = Column(Integer, ForeignKey("trn_usuario.id_usuario"))


class TablaPIV(Base):
    __tablename__ = "trn_piv_mensual"
    
    id_piv = Column(Integer, primary_key=True, index=True)
    mes = Column(String(20), nullable=False)
    anio = Column(Integer, nullable=False)
    parametro = Column(String(100), nullable=False)
    valor_obtenido = Column(Numeric(14, 4), nullable=False)


class TablaExtrasistema(Base):
    __tablename__ = "trn_extrasistema"
    
    id_extra = Column(Integer, primary_key=True, index=True)
    mes = Column(String(20), nullable=False)
    anio = Column(Integer, nullable=False)
    meta_asociada = Column(String(100), nullable=False)
    cantidad_atenciones = Column(Integer, nullable=False)


class TablaContinuidadIAAPS(Base):
    __tablename__ = "trn_continuidad_iaaps"
    
    id_cont = Column(Integer, primary_key=True, index=True)
    mes = Column(String(20), nullable=False)
    anio = Column(Integer, nullable=False)
    porcentaje_obtenido = Column(Numeric(5, 2), nullable=False)