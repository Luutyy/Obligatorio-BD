import { Link } from "react-router-dom"

async function getMetricas(codigo) {
    console.log(`/api/countries/${codigo}`)
    const response = await fetch(`/api/countries/${codigo}`);
    return(await response.json());
}

export function Metricas(){

    return(
        <div>
            <Link to={'/'}>⬅Volver</Link>
            <p>Datos datos y mas datos...</p>
        </div>
    )
}