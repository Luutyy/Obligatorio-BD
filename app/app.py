from fastapi import FastAPI, HTTPException

app = FastAPI()

from app.auth import router as auth_router
app.include_router(auth_router)

from app.metricas import torneo, equipo, jugadores, turnos, canchas, goles, puntos
<<<<<<< HEAD
from app.gets import complejosCanchas, equipos, facultad, jugadores, partidos, torneos, turnos
from app.ABM import equipo, jugador, partido
=======
from app.ABM import equipo, jugador, partido
from app.gets import complejosCanchas, equipos, facultad, jugadores, partidos, torneos, turnos
>>>>>>> 733894b5d3ccc804b453fd70aacbe97c10452074
