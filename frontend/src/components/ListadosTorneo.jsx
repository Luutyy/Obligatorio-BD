
import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import "./ListadosTorneo.css";

const API_URL = (
    process.env.REACT_APP_API_URL || "http://localhost:8000"
).replace(/\/+$/, "");

// Función común para consultar el backend
async function consultarAPI(endpoint) {
    const token = localStorage.getItem("token");

    const response = await fetch(`${API_URL}${endpoint}`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });

    if (!response.ok) {
        const mensaje = await response.text();
        throw new Error(`Error ${response.status}: ${mensaje}`);
    }

    return response.json();
}

// Hook compartido para obtener los torneos
function useTorneos() {
    const [torneos, setTorneos] = useState([]);
    const [torneoSeleccionado, setTorneoSeleccionado] = useState("");
    const [errorTorneos, setErrorTorneos] = useState("");

    useEffect(() => {
        let activo = true;

        async function cargar() {
            try {
                const datos = await consultarAPI("/torneos");

                if (activo) {
                    setTorneos(datos);

                    if (datos.length > 0) {
                        setTorneoSeleccionado(
                            String(datos[0].id_torneo)
                        );
                    }
                }
            } catch (error) {
                if (activo) setErrorTorneos(error.message);
            }
        }

        cargar();

        return () => {
            activo = false;
        };
    }, []);

    return {
        torneos,
        torneoSeleccionado,
        setTorneoSeleccionado,
        errorTorneos
    };
}

// Selector de torneo
function SelectorTorneo({
    torneos,
    seleccionado,
    cambiar
}) {
    return (
        <div className="selector-torneo-listado">
            <label htmlFor="torneo-listado">
                Seleccionar torneo:
            </label>

            <select
                id="torneo-listado"
                value={seleccionado}
                onChange={e => cambiar(e.target.value)}
            >
                {torneos.map(torneo => (
                    <option
                        key={torneo.id_torneo}
                        value={torneo.id_torneo}
                    >
                        {torneo.nombre} ({torneo.anio} -
                        Semestre {torneo.semestre})
                    </option>
                ))}
            </select>
        </div>
    );
}

// Encabezado compartido
function Encabezado({ titulo, children }) {
    return (
        <header className="listado-header">
            <Link to="/inicio">⬅ Volver al inicio</Link>
            <h1>{titulo}</h1>
            {children}
        </header>
    );
}

// ===============================
// JUGADORES
// ===============================

export function Jugadores() {
    const [jugadores, setJugadores] = useState([]);
    const [busqueda, setBusqueda] = useState("");
    const [cargando, setCargando] = useState(true);
    const [error, setError] = useState("");

    async function cargarJugadores() {
        setCargando(true);
        setError("");

        try {
            const datos = await consultarAPI("/jugadores");
            setJugadores(datos);
        } catch (error) {
            setError(error.message);
        } finally {
            setCargando(false);
        }
    }

    useEffect(() => {
        cargarJugadores();
    }, []);

    const jugadoresFiltrados = jugadores.filter(jugador => {
        const nombreCompleto =
            `${jugador.nombre} ${jugador.apellido}`.toLowerCase();

        return (
            nombreCompleto.includes(busqueda.toLowerCase()) ||
            String(jugador.ci).includes(busqueda) ||
            jugador.facultad.toLowerCase().includes(busqueda.toLowerCase())
        );
    });

    return (
        <div className="listado-page">
            <Encabezado titulo="Jugadores">
                <button onClick={cargarJugadores} disabled={cargando}>
                    {cargando ? "Cargando..." : "↻ Actualizar"}
                </button>
            </Encabezado>

            <main className="listado-contenido">
                <div className="listado-resumen">
                    <span>
                        Jugadores registrados: <strong>{jugadores.length}</strong>
                    </span>
                </div>

                <input
                    className="buscador-listado"
                    type="text"
                    placeholder="Buscar por nombre, apellido, CI o facultad..."
                    value={busqueda}
                    onChange={e => setBusqueda(e.target.value)}
                />

                {cargando && <p>Cargando jugadores...</p>}
                {error && <p className="listado-error">{error}</p>}

                {!cargando && !error && (
                    <div className="tabla-listado-container">
                        <table className="tabla-listado">
                            <thead>
                                <tr>
                                    <th>CI</th>
                                    <th>Nombre</th>
                                    <th>Apellido</th>
                                    <th>Facultad</th>
                                    <th>Tipo</th>
                                    <th>Fecha de nacimiento</th>
                                    <th>Acciones</th>
                                </tr>
                            </thead>

                            <tbody>
                                {jugadoresFiltrados.map(jugador => (
                                    <tr key={jugador.ci}>
                                        <td>{jugador.ci}</td>
                                        <td>{jugador.nombre}</td>
                                        <td>{jugador.apellido}</td>
                                        <td>{jugador.facultad}</td>
                                        <td>{jugador.tipo}</td>
                                        <td>{jugador.fecha_nacimiento}</td>
                                        <td>
                                            <Link
                                                className="enlace-detalle"
                                                to={`/jugadores/${jugador.ci}`}
                                            >
                                                Ver detalle
                                            </Link>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>

                        {jugadoresFiltrados.length === 0 && (
                            <p>No se encontraron jugadores.</p>
                        )}
                    </div>
                )}
            </main>
        </div>
    );
}

// ===============================
// EQUIPOS
// ===============================

export function Equipos() {
    const {
        torneos,
        torneoSeleccionado,
        setTorneoSeleccionado,
        errorTorneos
    } = useTorneos();

    const [equipos, setEquipos] = useState([]);
    const [facultades, setFacultades] = useState([]);
    const [busqueda, setBusqueda] = useState("");
    const [cargando, setCargando] = useState(false);
    const [error, setError] = useState("");

    useEffect(() => {
        if (!torneoSeleccionado) return;

        let activo = true;

        async function cargarEquipos() {
            setCargando(true);
            setError("");

            try {
                const [datosEquipos, datosFacultades] = await Promise.all([
                    consultarAPI(
                        `/equipos?id_torneo=${encodeURIComponent(torneoSeleccionado)}`
                    ),
                    consultarAPI("/facultades")
                ]);

                if (activo) {
                    setEquipos(datosEquipos);
                    setFacultades(datosFacultades);
                }
            } catch (error) {
                if (activo) setError(error.message);
            } finally {
                if (activo) setCargando(false);
            }
        }

        cargarEquipos();

        return () => {
            activo = false;
        };
    }, [torneoSeleccionado]);

    const equiposFiltrados = equipos.filter(equipo =>
        equipo.nombre.toLowerCase().includes(busqueda.toLowerCase())
    );

    function nombreFacultad(id) {
        const facultad = facultades.find(
            f => f.id_facultad === id
        );

        return facultad ? facultad.nombre : `Facultad ${id}`;
    }

    return (
        <div className="listado-page">
            <Encabezado titulo="Equipos">
                <SelectorTorneo
                    torneos={torneos}
                    seleccionado={torneoSeleccionado}
                    cambiar={setTorneoSeleccionado}
                />
            </Encabezado>

            <main className="listado-contenido">
                {errorTorneos && (
                    <p className="listado-error">{errorTorneos}</p>
                )}

                <div className="listado-resumen">
                    Equipos del torneo: <strong>{equipos.length}</strong>
                </div>

                <input
                    className="buscador-listado"
                    placeholder="Buscar equipo..."
                    value={busqueda}
                    onChange={e => setBusqueda(e.target.value)}
                />

                {cargando && <p>Cargando equipos...</p>}
                {error && <p className="listado-error">{error}</p>}

                {!cargando && !error && (
                    <div className="tabla-listado-container">
                        <table className="tabla-listado">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Equipo</th>
                                    <th>Facultad</th>
                                    <th>CI del capitán</th>
                                    <th>Acciones</th>
                                </tr>
                            </thead>

                            <tbody>
                                {equiposFiltrados.map(equipo => (
                                    <tr key={equipo.id_equipo}>
                                        <td>{equipo.id_equipo}</td>
                                        <td>{equipo.nombre}</td>
                                        <td>{nombreFacultad(equipo.id_facultad)}</td>
                                        <td>{equipo.ci_capitan}</td>
                                        <td>
                                            <Link
                                                className="enlace-detalle"
                                                to={`/equipos/${equipo.id_equipo}`}
                                            >
                                                Ver equipo
                                            </Link>
                                            {" | "}
                                            <Link
                                                className="enlace-detalle"
                                                to={`/equipos/${equipo.id_equipo}/plantel`}
                                            >
                                                Ver plantel
                                            </Link>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>

                        {equiposFiltrados.length === 0 && (
                            <p>No se encontraron equipos.</p>
                        )}
                    </div>
                )}
            </main>
        </div>
    );
}

// ===============================
// FECHAS Y PARTIDOS
// ===============================

export function Fechas() {
    const {
        torneos,
        torneoSeleccionado,
        setTorneoSeleccionado,
        errorTorneos
    } = useTorneos();

    const [partidos, setPartidos] = useState([]);
    const [equipos, setEquipos] = useState([]);
    const [cargando, setCargando] = useState(false);
    const [error, setError] = useState("");

    useEffect(() => {
        if (!torneoSeleccionado) return;

        let activo = true;

        async function cargarDatos() {
            setCargando(true);
            setError("");

            try {
                const [datosPartidos, datosEquipos] = await Promise.all([
                    consultarAPI(
                        `/partidos?id_torneo=${encodeURIComponent(torneoSeleccionado)}`
                    ),
                    consultarAPI(
                        `/equipos?id_torneo=${encodeURIComponent(torneoSeleccionado)}`
                    )
                ]);

                if (activo) {
                    setPartidos(datosPartidos);
                    setEquipos(datosEquipos);
                }
            } catch (error) {
                if (activo) setError(error.message);
            } finally {
                if (activo) setCargando(false);
            }
        }

        cargarDatos();

        return () => {
            activo = false;
        };
    }, [torneoSeleccionado]);

    function nombreEquipo(id) {
        const equipo = equipos.find(
            e => e.id_equipo === id
        );

        return equipo ? equipo.nombre : `Equipo ${id}`;
    }

    const fechas = [...new Set(
        partidos.map(partido => partido.numero_fecha)
    )].sort((a, b) => a - b);

    return (
        <div className="listado-page">
            <Encabezado titulo="Fechas y partidos">
                <SelectorTorneo
                    torneos={torneos}
                    seleccionado={torneoSeleccionado}
                    cambiar={setTorneoSeleccionado}
                />
            </Encabezado>

            <main className="listado-contenido">
                {errorTorneos && (
                    <p className="listado-error">{errorTorneos}</p>
                )}

                <div className="listado-resumen">
                    Partidos registrados: <strong>{partidos.length}</strong>
                </div>

                {cargando && <p>Cargando partidos...</p>}
                {error && <p className="listado-error">{error}</p>}

                {!cargando && !error && fechas.map(numeroFecha => {
                    const partidosFecha = partidos
                        .filter(p => p.numero_fecha === numeroFecha)
                        .sort((a, b) => a.dia.localeCompare(b.dia));

                    return (
                        <section
                            className="fecha-card"
                            key={numeroFecha}
                        >
                            <h2>Fecha {numeroFecha}</h2>

                            <div className="partidos-grid">
                                {partidosFecha.map(partido => (
                                    <article
                                        className="partido-card"
                                        key={partido.id_partido}
                                    >
                                        <div className="partido-equipos">
                                            <span>
                                                {nombreEquipo(partido.id_equipo_local)}
                                            </span>

                                            <strong>VS</strong>

                                            <span>
                                                {nombreEquipo(partido.id_equipo_visitante)}
                                            </span>
                                        </div>

                                        <p>
                                            <strong>Fecha:</strong> {partido.dia}
                                        </p>

                                        <p>
                                            <strong>Cancha:</strong> {partido.nombre_cancha}
                                        </p>

                                        <p>
                                            <strong>Complejo:</strong> {partido.id_complejo}
                                        </p>

                                        <p>
                                            <strong>Turno:</strong> {partido.id_turno}
                                        </p>

                                        <span className={`estado-partido estado-${partido.estado}`}>
                                            {partido.estado}
                                        </span>

                                        <Link
                                            className="enlace-detalle"
                                            to={`/partidos/${partido.id_partido}`}
                                        >
                                            Ver partido →
                                        </Link>
                                    </article>
                                ))}
                            </div>
                        </section>
                    );
                })}

                {!cargando && !error && partidos.length === 0 && (
                    <p>No hay partidos para este torneo.</p>
                )}
            </main>
        </div>
    );
}

export function Facultades() {
    const [facultades, setFacultades] = useState([]);
    const [cargando, setCargando] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        async function cargarFacultades() {
            try {
                const datos = await consultarAPI("/facultades");
                setFacultades(datos);
            } catch (err) {
                setError(err.message);
            } finally {
                setCargando(false);
            }
        }

        cargarFacultades();
    }, []);

    return (
        <div className="listado-container">
            <Encabezado
                titulo="Facultades"
                descripcion="Seleccioná una facultad para consultar sus equipos."
            />

            {cargando && <p>Cargando facultades...</p>}
            {error && <p className="error-mensaje">{error}</p>}

            {!cargando && !error && (
                <div className="facultades-grid">
                    {facultades.map((facultad) => (
                        <Link
                            key={facultad.id_facultad}
                            to={`/facultades/${facultad.id_facultad}/equipos`}
                            className="facultad-card"
                        >
                            <span className="facultad-icono">🏛️</span>

                            <h2>{facultad.nombre}</h2>

                            <span className="facultad-enlace">
                                Ver equipos →
                            </span>
                        </Link>
                    ))}
                </div>
            )}
        </div>
    );
}
export function EquiposFacultad() {
    const { id } = useParams();

    const {
        torneos,
        torneoSeleccionado,
        setTorneoSeleccionado
    } = useTorneos();

    const [facultad, setFacultad] = useState(null);
    const [equipos, setEquipos] = useState([]);
    const [cargando, setCargando] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        let activo = true;

        async function cargarDatos() {
            if (!torneoSeleccionado) return;

            setCargando(true);
            setError("");

            try {
                const [facultades, todosLosEquipos] = await Promise.all([
                    consultarAPI("/facultades"),
                    consultarAPI(`/equipos?id_torneo=${torneoSeleccionado}`)
                ]);

                if (!activo) return;

                const facultadEncontrada = facultades.find(
                    f => f.id_facultad === Number(id)
                );

                const equiposFiltrados = todosLosEquipos.filter(
                    equipo => equipo.id_facultad === Number(id)
                );

                setFacultad(facultadEncontrada);
                setEquipos(equiposFiltrados);

            } catch (err) {
                if (activo) setError(err.message);
            } finally {
                if (activo) setCargando(false);
            }
        }

        cargarDatos();

        return () => {
            activo = false;
        };
    }, [id, torneoSeleccionado]);

    return (
        <div className="listado-container">
            <Link to="/facultades" className="volver-link">
                ← Volver a facultades
            </Link>

            <Encabezado
                titulo={facultad?.nombre || "Equipos de la facultad"}
                descripcion="Equipos participantes de esta facultad."
            />

            <SelectorTorneo
                torneos={torneos}
                torneoSeleccionado={torneoSeleccionado}
                setTorneoSeleccionado={setTorneoSeleccionado}
            />

            {cargando && <p>Cargando equipos...</p>}
            {error && <p className="error-mensaje">{error}</p>}

            {!cargando && !error && (
                <>
                    <p className="cantidad-resultados">
                        {equipos.length} equipo(s) encontrado(s)
                    </p>

                    {equipos.length === 0 ? (
                        <p className="sin-resultados">
                            Esta facultad no tiene equipos registrados en este torneo.
                        </p>
                    ) : (
                        <div className="equipos-facultad-grid">
                            {equipos.map(equipo => (
                                <div
                                    key={equipo.id_equipo}
                                    className="equipo-facultad-card"
                                >
                                    <span className="equipo-icono">⚽</span>

                                    <h2>{equipo.nombre}</h2>

                                    <p>
                                        <strong>Capitán:</strong>{" "}
                                        {equipo.ci_capitan}
                                    </p>

                                    <Link to={`/equipos/${equipo.id_equipo}`}>
                                        Ver equipo →
                                    </Link>

                                    <Link to={`/equipos/${equipo.id_equipo}/plantel`}>
                                        Ver plantel
                                    </Link>
                                </div>
                            ))}
                        </div>
                    )}
                </>
            )}
        </div>
    );
}