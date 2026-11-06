from app.app import app
from ..conexion import conexion

@app.get('/metricas/puntos_fair_play')
def puntos_fair_play():
    sql = """
        SELECT e.nombre, e.id_equipo, SUM( CASE WHEN t.color='amarilla' THEN 1 WHEN t.color='roja' THEN 3 ELSE 0 END) as puntos,e.id_torneo
        FROM torneo.tarjeta t JOIN torneo.planilla_partido pp ON t.id_partido = pp.id_partido AND t.ci_jugador = pp.ci_jugador
                              RIGHT JOIN torneo.equipo e on pp.id_equipo = e.id_equipo
        GROUP BY id_equipo, e.id_torneo
        ORDER BY puntos;
    """

    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql,)
    resultado = cursor.fetchall()
    cursor.close()

    return resultado

@app.get('/metricas/tabla_torneo')
def tabla_torneo(id_torneo: int):
    sql = """
        SELECT e.id_equipo, e.nombre, SUM(pp.puntos) AS puntos_totales, e.id_torneo
        FROM puntos_partido pp
        JOIN equipo e ON pp.id_equipo=e.id_equipo
        WHERE e.id_torneo = %s
        GROUP BY id_equipo, e.id_torneo
        ORDER BY e.id_torneo, puntos_totales DESC;
    """
    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql,(id_torneo,))
    resultado = cursor.fetchall()
    cursor.close()

    return resultado