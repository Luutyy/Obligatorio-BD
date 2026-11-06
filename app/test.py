import app.metricas.torneo as torneo;
import app.metricas.equipo as equipo;
import app.metricas.jugadores as jugadores;
import app.metricas.turnos as turnos
import app.metricas.canchas as canchas
import app.metricas.goles as goles
import app.metricas.puntos as puntos

porcentaje_partidas = torneo.porcentaje_partidos(1)
cantidad_sanciones = equipo.cantidad_sanciones(1)
jugadores_sin_plantilla = jugadores.jugadores_sin_plantilla(1)
jugador_tipo = jugadores.jugador_por_facultad_tipo()
goles_por_torneo = goles.goles_por_torneo()
puntos_fair_play = puntos.puntos_fair_play()
goleadores = jugadores.goleadores(1)
turnos_mas_usados = turnos.turnos_mas_utilizados()
canchas_mas_usadas = canchas.canchas_mas_usadas()
tabla_torneo = puntos.tabla_torneo(1)
ultima_fecha = torneo.partidos_ultima_fecha(1)
goles_a_favor = equipo.goles_a_favor(1)
promedio_goles_por_equipo = equipo.promedio_por_equipo(1)

#print(porcentaje_partidas)
#print(f"Total: {porcentaje_partidas['total']}")
#print(f"Jugados: {porcentaje_partidas['jugados']}")
#print(f"Cancelados: {porcentaje_partidas['cancelados']}")
#print(f"Postergados: {porcentaje_partidas['postergados']}")
#print(f"Programados: {porcentaje_partidas['programados']}")
#print(f"Porcentaje de partidos jugados: {porcentaje_partidas['porcentaje_jugados']}%")
#print(f"Porcentaje cancelados/programados: {porcentaje_partidas['porcentaje_cancelados_y_postergados']}%")
#
#print(cantidad_sanciones)
#print(jugadores_sin_plantilla)
#print(jugador_tipo)

#print(goles_por_torneo)
#print(puntos_fair_play)
#print(goleadores)
#print(turnos_mas_usados)
#print(canchas_mas_usadas)
#print(tabla_torneo)
#print(ultima_fecha)
#print(goles_a_favor)
print(promedio_goles_por_equipo)