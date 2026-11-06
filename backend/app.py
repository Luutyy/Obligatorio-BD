from fastapi import FastAPI, HTTPException

app = FastAPI()

from backend.auth import router as auth_router
app.include_router(auth_router)

from backend.metricas import torneo, equipo, jugadores, turnos, canchas, goles, puntos
from backend.gets import complejosCanchas, equipos, facultad, jugadores, partidos, torneos, turnos
from backend.ABM import equipo, jugador, partido, cancha, usuarios, planilla, complejo, equipo_jugador_torneo, gol, sancion, tarjeta
