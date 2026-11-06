from ..conexion import conexion
from backend.app import app

@app.get('/metricas/porcentaje_partidos')
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
    resultado = cursor.fetchall()
    cursor.close()

    return resultado


# Metrica agregada: ver los resultados de la ultima fecha
@app.get('/metricas/ultima-fecha')
def partidos_ultima_fecha(id_torneo: int):
    sql = """
        SELECT 
            p.id_partido,
            p.numero_fecha,
            el.nombre AS equipo_local,
            rp.goles_local,
            ev.nombre AS equipo_visitante,
            rp.goles_visitante
        FROM torneo.partidos_jugados p
        JOIN torneo.resultado_partido rp
            ON rp.id_partido = p.id_partido
        JOIN torneo.equipo el
            ON el.id_equipo = p.id_equipo_local
        JOIN torneo.equipo ev
            ON ev.id_equipo = p.id_equipo_visitante
        WHERE p.numero_fecha = (
            SELECT
                MAX(numero_fecha)
                FROM torneo.partidos_jugados
                WHERE id_torneo = %s
            )
            AND p.id_torneo = %s
        ORDER BY p.id_partido
    """

    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql, (id_torneo, id_torneo))
    resultado = cursor.fetchall()
    cursor.close()

    return resultado