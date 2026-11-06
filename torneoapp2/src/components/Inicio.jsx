import { Link } from "react-router-dom";

export function Inicio(){
    return(
        <view>
            <div>
                <p>Bienvenid@ al torneo</p>
                <div>
                    <Link to={'/Facultades'}>Ver facultades</Link>
                </div>
                <div>
                    <Link to={'/Fechas'}>Ver fechas</Link>
                </div>
                <div>
                    <Link to={'/Jugadores'}>Ver jugadores</Link>
                </div>
                <div>
                    <Link to={'/Metricas'}>Ver Metricas</Link>
                </div>
            </div>
        </view>
    )
}