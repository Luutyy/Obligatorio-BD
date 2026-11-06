from fastapi import FastAPI, HTTPException

app = FastAPI()

from app.metricas import torneo, equipo, jugadores, turnos, canchas, goles, puntos