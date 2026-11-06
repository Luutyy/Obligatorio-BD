import { Link } from "react-router-dom"
import { Jugador } from "./Jugador"

export function Jugadores(){
    return(
        <div>
            <Link to={'/'}>⬅Volver</Link>
            <p>Aca va a aparecer una lista de jugadores</p>
            <Jugador></Jugador>
            <Jugador></Jugador>
        </div>
    )
}