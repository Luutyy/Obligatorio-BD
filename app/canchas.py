from conexion import conexion

#@app.get('/metricas/canchas')
def canchas_mas_usadas():
    sql = """
        SELECT CONCAT(p.nombre_cancha,' - ', c.nombre_complejo) AS cancha, COUNT(*) as veces_usada
            FROM torneo.partido p JOIN torneo.complejo c on p.id_complejo = c.id_complejo
            GROUP BY c.id_complejo, p.nombre_cancha
            ORDER BY veces_usada DESC;
    """

    cursor = conexion.cursor(dictionary=True)
    cursor.execute(sql)
    resultado = cursor.fetchall()
    cursor.close()

    return resultado
    