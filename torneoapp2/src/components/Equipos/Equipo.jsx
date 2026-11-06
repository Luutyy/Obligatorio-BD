import { Link } from "react-router-dom"

export function Equipo(equipo){
    return(
        <div>
            <Link to={'/Equipos'}>⬅Volver</Link>
            <p>Este es un equipo</p>
        </div>
    )
}