from fastapi import FastAPI, HTTPException

app = FastAPI()
@app.get("/")
def inicio():
    return {"mensaje": "API funcionando correctamente"}

from app.metricas import torneo, equipo, jugadores, turnos, canchas, goles, puntos