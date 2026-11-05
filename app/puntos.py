from conexion import conexion

#@app.get('/metricas/puntos_fair_play')
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