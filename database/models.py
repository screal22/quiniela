from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from database.connection import Base
from datetime import datetime, UTC
import uuid

class Partidos(Base):
    __tablename__ = "partidos"

    id = Column(String, primary_key=True, index=True)
    nom_partido = Column(String, nullable=False)
    fecha_partido = Column(DateTime)
    added_date = Column(DateTime, default=lambda: datetime.now(UTC))

class Pronosticos(Base):
    __tablename__ = "pronosticos"

    __table_args__ = (
        UniqueConstraint(
            'participante',
            'id_partido',
            name='uq_pronostico_participante_partido'
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    id_partido = Column(String, ForeignKey('partidos.id'))
    pronostico_1 = Column(Integer, nullable=True)
    pronostico_2 = Column(Integer, nullable=True)
    participante = Column(String)
    added_date = Column(DateTime, default=lambda: datetime.now(UTC))

class ResultadosPartidos(Base):
    __tablename__ = "resultados_partidos"

    __table_args__ = (
        UniqueConstraint(
            'id_partido',
            name='uq_resultados_partidos'
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    id_partido = Column(String, ForeignKey('partidos.id'))
    resultado_1 = Column(Integer, nullable=True)
    resultado_2 = Column(Integer, nullable=True)
    added_date = Column(DateTime, default=lambda: datetime.now(UTC))