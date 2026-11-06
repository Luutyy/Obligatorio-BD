import { Link } from "react-router-dom";

export function TarjetaEquipo(){
    return(
        <div>
            <p>Equipo 1</p>
            <Link to={'/Equipo'}>Ver equipo</Link>
        </div>
    )
}