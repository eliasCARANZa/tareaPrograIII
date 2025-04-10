from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from bd_models import Personaje, Mision, Base
from cola import Cola

app = FastAPI()

DB_URL = "sqlite:///./test.db"
motor = create_engine(DB_URL, connect_args={"check_same_thread": False})
Sesion = sessionmaker(bind=motor)

Base.metadata.create_all(bind=motor)

misiones_por_personaje = {}

class DatosPersonaje(BaseModel):
    nombre: str
    nivel: int

class DatosMision(BaseModel):
    nombre: str
    descripcion: str
    nivel_requerido: int

@app.post("/personajes/")
def nuevo_personaje(datos: DatosPersonaje):
    db = Sesion()
    personaje = Personaje(nombre=datos.nombre, nivel=datos.nivel)
    db.add(personaje)
    db.commit()
    db.refresh(personaje)
    misiones_por_personaje[personaje.id] = Cola()
    return personaje

@app.post("/misiones/")
def nueva_mision(datos: DatosMision):
    db = Sesion()
    mision = Mision(
        nombre=datos.nombre,
        descripcion=datos.descripcion,
        nivel_requerido=datos.nivel_requerido
    )
    db.add(mision)
    db.commit()
    db.refresh(mision)
    return mision

@app.post("/personajes/{pid}/misiones/{mid}")
def asignar_mision(pid: int, mid: int):
    db = Sesion()
    p = db.query(Personaje).filter_by(id=pid).first()
    m = db.query(Mision).filter_by(id=mid).first()

    if not p or not m:
        raise HTTPException(status_code=404, detail="No encontrado")

    p.misiones.append(m)
    db.commit()

    if pid not in misiones_por_personaje:
        misiones_por_personaje[pid] = Cola()
    misiones_por_personaje[pid].agregar(m.nombre)

    return {"message": f"Misión '{m.nombre}' asignada a {p.nombre}"}

@app.post("/personajes/{pid}/completar")
def completar(pid: int):
    db = Sesion()
    p = db.query(Personaje).filter_by(id=pid).first()

    if pid not in misiones_por_personaje or misiones_por_personaje[pid].esta_vacia():
        raise HTTPException(status_code=404, detail="Sin misiones")

    m_realizada = misiones_por_personaje[pid].quitar()
    puntos = 10
    p.xp += puntos
    db.commit()

    return {"message": f"Misión completada: {m_realizada}. {p.nombre} gana {puntos} XP."}

@app.get("/personajes/{pid}/misiones")
def listar_misiones(pid: int):
    if pid not in misiones_por_personaje:
        return {"misiones": []}
    return {"misiones": misiones_por_personaje[pid]._datos}
