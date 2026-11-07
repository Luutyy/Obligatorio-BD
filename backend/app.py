from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from backend.auth import router as auth_router
app.include_router(auth_router)

from backend.metricas import torneo, equipo, jugadores, turnos, canchas, goles, puntos
from backend.gets import complejosCanchas, equipos, facultad, jugadores, partidos, torneos, turnos
from backend.ABM import equipo, jugador, partido, cancha, usuarios, planilla, complejo, equipo_jugador_torneo, gol, sancion, tarjeta
