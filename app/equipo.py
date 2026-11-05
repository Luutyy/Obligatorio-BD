from conexion import conexion

#@app.get('/metricas/cantidad_sanciones')
def cantidad_sanciones(id_torneo: int):
    sql = """
        SELECT
            e.nombre AS equipo,
            s.motivo AS motivo,
            COUNT(*) as cantidad_sanciones
        FROM sancion_jugador s
        JOIN equipo_jugador_torneo ejt
            ON ejt.ci_jugador = s.ci_jugador
            AND ejt.id_torneo = s.id_torneo
        JOIN equipo e 
            ON e.id_equipo = ejt.id_equipo
        WHERE s.id_torneo = %s
        GROUP BY e.id_equipo, e.nombre, s.motivo
        ORDER BY e.nombre, s.motivo
    """

    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql, (id_torneo,))
    resultado = cursor.fetchall()
    cursor.close()

    return resultado


    
