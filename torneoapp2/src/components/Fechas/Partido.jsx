import { Link } from "react-router-dom"

export function Partido(partido){
    return(
        <div>
            <Link to={'/Fecha'}>⬅Volver</Link>
            <p>Este es un equipo</p>
        </div>
    )
}