from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

vinculo = Table(
    'relacion_pm',
    Base.metadata,
    Column('pid', Integer, ForeignKey('pj.id')),
    Column('mid', Integer, ForeignKey('ms.id'))
)

class Personaje(Base):
    __tablename__ = 'pj'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    nivel = Column(Integer, nullable=False)
    xp = Column(Integer, default=0)

    misiones = relationship("Mision", secondary=vinculo, back_populates="personajes")

class Mision(Base):
    __tablename__ = 'ms'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    nivel_requerido = Column(Integer, nullable=False)

    personajes = relationship("Personaje", secondary=vinculo, back_populates="misiones")
