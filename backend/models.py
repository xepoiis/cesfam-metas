from sqlalchemy import Column, Integer, String, Numeric
from database import Base

class TablaPIV(Base):
    __tablename__ = "trn_piv_mensual"

    id_piv = Column(Integer, primary_key=True, index=True)
    mes = Column(String(20), nullable=False)
    anio = Column(Integer, nullable=False)
    parametro = Column(String(100), nullable=False)
    valor_obtenido = Column(Numeric(14, 4), nullable=False)