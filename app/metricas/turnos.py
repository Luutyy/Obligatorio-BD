from ..conexion import conexion


#@app.get('/metricas/turnos')
def turnos_mas_utilizados():
    sql = """
        SELECT CONCAT(t.hora_inicio,' - ', t.hora_fin) AS turno, COUNT(*) as veces_usado
            FROM torneo.partido p JOIN torneo.turno t on p.id_turno = t.id_turno
            GROUP BY t.id_turno
            ORDER BY veces_usado DESC;
    """

    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql)
    resultado = cursor.fetchall()
    cursor.close()

    return resultado
    