import { Link } from "react-router-dom"

export function Facultades(){
    return(
        <div>
            <Link to={'/'}>⬅Volver</Link>
            <p>Estas son las facultades</p>
            <Link to={'/Equipos'}>Facultad 1</Link>
            <Link to={'/Equipos'}>Facultad 2</Link>
            <Link to={'/Equipos'}>Facultad 3</Link>
        </div>
    )
}