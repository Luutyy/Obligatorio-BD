import { Link } from "react-router-dom"

export function Fecha(fecha){
    return(
        <div>
            <Link to={'/Fechas'}>⬅Volver</Link>
            <p>Esta es una fecha</p>
        </div>
    )
}