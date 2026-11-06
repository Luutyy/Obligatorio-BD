from ..conexion import conexion
from app.app import app

@app.get('/metricas/jugadores_sin_plantilla')
def jugadores_sin_plantilla(id_torneo: int):
    sql = """
        SELECT
            j.ci,
            j.nombre,
            j.apellido,
            e.nombre AS equipo,
            ejt.numero_camiseta
        FROM equipo_jugador_torneo ejt
        JOIN equipo e ON e.id_equipo = ejt.id_equipo 
        JOIN jugador j ON j.ci = ejt.ci_jugador
        WHERE ejt.id_torneo = %s
            AND NOT EXISTS (
                SELECT p.id_partido
                    FROM planilla_partido pp
                    JOIN partido p ON p.id_partido = pp.id_partido
                    WHERE pp.ci_jugador = ejt.ci_jugador AND p.id_torneo = ejt.id_torneo
                    )
                ORDER BY e.nombre, j.apellido, j.nombre
    """

    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql, (id_torneo,))
    resultado = cursor.fetchall()
    cursor.close()

    return resultado

@app.get('/metricas/jugador_facultad_tipo')
def jugador_por_facultad_tipo():
    sql = """
        SELECT 
            f.nombre AS facultad,
            j.tipo AS tipo,
            COUNT(*) AS cantidad
        FROM jugador j
        JOIN facultad f on f.id_facultad = j.id_facultad
        GROUP BY f.id_facultad, f.nombre, j.tipo
        ORDER BY f.nombre, j.tipo
    """
    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql)
    resultado = cursor.fetchall()
    cursor.close()

    return resultado

@app.get('/metricas/goleadores')
def goleadores(id_torneo: int):
    sql = """
        SELECT
            CONCAT(j.nombre, ' ', j.apellido) AS nombre_completo,
            j.ci,
            COUNT(*) AS cantidad_goles
        FROM torneo.gol g
        JOIN torneo.jugador j
            ON g.ci_jugador = j.ci
        JOIN torneo.partido p
            ON g.id_partido = p.id_partido
        WHERE p.id_torneo = %s
          AND g.autogol = FALSE
        GROUP BY g.ci_jugador, j.nombre, j.apellido
        ORDER BY cantidad_goles DESC
        LIMIT 10;
        """
    
    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql, (id_torneo,))
    resultado = cursor.fetchall()
    cursor.close()

    return resultado