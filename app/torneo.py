from conexion import conexion

#@app.get('/metricas/porcentaje_partidos')
def porcentaje_partidos(id_torneo: int):
    sql = """
        SELECT
            COUNT(*) AS total,
            COALESCE(SUM(estado = 'jugado'), 0) AS jugados,
            COALESCE(SUM(estado = 'postergado'), 0) AS postergados,
            COALESCE(SUM(estado = 'cancelado'), 0) AS cancelados,
            COALESCE(SUM(estado = 'programado'), 0) AS programados,

            COALESCE(
                ROUND(
                    SUM(estado = 'jugado') / COUNT(*) * 100, 2
                ),0
            ) AS porcentaje_jugados,
                

            COALESCE(
                ROUND(
                    (SUM(estado = 'cancelado') + SUM(estado = 'postergado')) / COUNT(*) * 100, 2
                ), 0
            ) AS porcentaje_cancelados_y_postergados

        FROM partido
        WHERE id_torneo = %s
    """

    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql, (id_torneo,))
    resultado = cursor.fetchone()
    cursor.close()

    return resultado
