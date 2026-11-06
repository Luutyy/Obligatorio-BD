from ..conexion import conexion
from app.app import app

@app.get('/metricas/promedio_goles_torneo')
def goles_por_torneo():
    sql = """
        SELECT p.id_torneo,AVG(gp.total_goles) AS promedio_goles
        FROM partidos_jugados p 
        LEFT JOIN (SELECT id_partido,SUM(cantidad_goles) AS total_goles
                                             FROM goles_partido
                                             GROUP BY id_partido) gp ON p.id_partido = gp.id_partido
        GROUP BY p.id_torneo;
    """

    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql,)
    resultado = cursor.fetchall()
    cursor.close()#srfggsfdz

    return resultado

@app.get('/metricas/promedio_goles_fecha')
def goles_por_fechas():
    sql = """
        SELECT
        p.id_torneo, p.numero_fecha,AVG(gp.total_goles) AS promedio_goles
        FROM torneo.partidos_jugados p JOIN (SELECT id_partido,SUM(cantidad_goles) AS total_goles
                                    FROM torneo.goles_partido
                                    GROUP BY id_partido) gp ON p.id_partido = gp.id_partido
        GROUP BY p.id_torneo, p.numero_fecha;
    """

    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql,)
    resultado = cursor.fetchall()
    cursor.close()#srfggsfdz