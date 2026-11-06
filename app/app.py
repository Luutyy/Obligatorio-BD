from fastapi import FastAPI, HTTPException

app = FastAPI()
@app.get("/")
def inicio():
    return {"mensaje": "API funcionando correctamente"}

from app.metricas import torneo, equipo, jugadores, turnos, canchas, goles, puntos
from app.ABM import equipo, jugador, partido
from app.gets import complejosCanchas, equipos, facultad, jugadores, partidos, torneos, turnos
