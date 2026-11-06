
import { Link, useNavigate } from "react-router-dom";
import "./Inicio.css";

export function Inicio() {

    const navigate = useNavigate();

    const token = localStorage.getItem("token");
    const rol = localStorage.getItem("rol");

    function cerrarSesion() {
        localStorage.removeItem("token");
        localStorage.removeItem("rol");
        navigate("/login");
    }

    const secciones = [
        {
            titulo: "Facultades",
            descripcion: "Consultá las facultades participantes del torneo.",
            icono: "🏛️",
            ruta: "/Facultades"
        },
        {
            titulo: "Fechas",
            descripcion: "Revisá las fechas y los partidos programados.",
            icono: "📅",
            ruta: "/Fechas"
        },
        {
            titulo: "Jugadores",
            descripcion: "Conocé a los jugadores y sus equipos.",
            icono: "⚽",
            ruta: "/Jugadores"
        },
        {
            titulo: "Métricas",
            descripcion: "Explorá estadísticas y datos del torneo.",
            icono: "📊",
            ruta: "/Metricas"
        }
    ];

    return (
        <div className="inicio">

            {/* ENCABEZADO */}
            <header className="inicio-header">

                <Link to="/inicio" className="logo-torneo">
                    <span>⚽</span>
                    TORNEO APP
                </Link>

                <nav className="inicio-nav">

                    {token ? (
                        <>
                            <span className="usuario-rol">
                                {rol}
                            </span>

                            <button
                                className="boton-sesion"
                                onClick={cerrarSesion}
                            >
                                Cerrar sesión
                            </button>
                        </>
                    ) : (
                        <Link to="/login" className="boton-sesion">
                            Iniciar sesión
                        </Link>
                    )}

                </nav>

            </header>

            {/* PRESENTACIÓN */}
            <main>

                <section className="inicio-hero">

                    <div className="hero-contenido">

                        <span className="hero-etiqueta">
                            ⚽ TEMPORADA DEPORTIVA
                        </span>

                        <h1>
                            Bienvenido al <span>torneo</span>
                        </h1>

                        <p>
                            Toda la información de la competencia en un
                            solo lugar. Consultá equipos, jugadores,
                            partidos y estadísticas.
                        </p>

                        {!token && (
                            <Link to="/login" className="hero-boton">
                                Acceder a mi cuenta →
                            </Link>
                        )}

                    </div>

                    <div className="hero-icono">
                        ⚽
                    </div>

                </section>

                {/* SECCIONES */}
                <section className="secciones">

                    <div className="secciones-titulo">
                        <h2>Explorá el torneo</h2>
                        <p>Seleccioná una sección para continuar.</p>
                    </div>

                    <div className="secciones-grid">

                        {secciones.map((seccion) => (

                            <Link
                                to={seccion.ruta}
                                className="seccion-card"
                                key={seccion.titulo}
                            >

                                <div className="seccion-icono">
                                    {seccion.icono}
                                </div>

                                <h3>{seccion.titulo}</h3>

                                <p>{seccion.descripcion}</p>

                                <span className="seccion-link">
                                    Ver sección →
                                </span>

                            </Link>

                        ))}

                    </div>

                </section>

            </main>

            {/* PIE DE PÁGINA */}
            <footer className="inicio-footer">
                <p>TORNEO APP · Sistema de gestión deportiva</p>
            </footer>

        </div>
    );
}
