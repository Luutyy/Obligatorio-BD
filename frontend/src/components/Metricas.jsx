
import { useState, useEffect, useCallback } from "react";
import "./Metricas.css";

const API_URL = (
    process.env.REACT_APP_API_URL || "http://localhost:8000"
).replace(/\/+$/, "");
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

export function Metricas() {
    const [torneos, setTorneos] = useState([]);
    const [torneoSeleccionado, setTorneoSeleccionado] = useState("");

    const [metricas, setMetricas] = useState([]);
    const [cargando, setCargando] = useState(false);
    const [error, setError] = useState("");

    // Endpoints disponibles
    const endpoints = [
        {
            nombre: "Porcentaje de partidos",
            endpoint: "/metricas/porcentaje_partidos",
            requiereTorneo: true
        },
        {
            nombre: "Última fecha",
            endpoint: "/metricas/ultima-fecha",
            requiereTorneo: true
        },
        {
            nombre: "Cantidad de sanciones",
            endpoint: "/metricas/cantidad_sanciones",
            requiereTorneo: true
        },
        {
            nombre: "Goles a favor",
            endpoint: "/metricas/goles_favor",
            requiereTorneo: true
        },
        {
            nombre: "Promedio por equipo",
            endpoint: "/metricas/promedio_equipo",
            requiereTorneo: true
        },
        {
            nombre: "Jugadores sin plantilla",
            endpoint: "/metricas/jugadores_sin_plantilla",
            requiereTorneo: true
        },
        {
            nombre: "Jugadores por facultad y tipo",
            endpoint: "/metricas/jugador_facultad_tipo",
            requiereTorneo: true
        },
        {
            nombre: "Goleadores",
            endpoint: "/metricas/goleadores",
            requiereTorneo: true
        },
        {
            nombre: "Turnos",
            endpoint: "/metricas/turnos",
            requiereTorneo: true
        },
        {
            nombre: "Canchas",
            endpoint: "/metricas/canchas",
            requiereTorneo: true
        },
        {
            nombre: "Promedio de goles por torneo",
            endpoint: "/metricas/promedio_goles_torneo",
            requiereTorneo: true
        },
        {
            nombre: "Promedio de goles por fecha",
            endpoint: "/metricas/promedio_goles_fecha",
            requiereTorneo: true
        },
        {
            nombre: "Puntos Fair Play",
            endpoint: "/metricas/puntos_fair_play",
            requiereTorneo: true
        },
        {
            nombre: "Tabla del torneo",
            endpoint: "/metricas/tabla_torneo",
            requiereTorneo: true
        }
    ];

    // Cargar torneos
    const cargarTorneos = useCallback(async () => {
        try {
            const datos = await consultarAPI("/torneos");

            setTorneos(datos);

            if (datos.length > 0) {
                setTorneoSeleccionado(String(datos[0].id_torneo));
            }
        } catch (err) {
            setError("No se pudieron cargar los torneos: " + err.message);
        }
    }, []);

    useEffect(() => {
        cargarTorneos();
    }, [cargarTorneos]);

    // Cargar métricas
    const cargarMetricas = useCallback(async () => {
        if (!torneoSeleccionado) return;

        setCargando(true);
        setError("");

        try {
            const resultados = await Promise.all(
                endpoints.map(async (item) => {
                    try {
                        const endpoint = item.requiereTorneo
                            ? `${item.endpoint}?id_torneo=${torneoSeleccionado}`
                            : item.endpoint;

                        const datos = await consultarAPI(endpoint);

                        return {
                            nombre: item.nombre,
                            datos,
                            error: null
                        };
                    } catch (err) {
                        return {
                            nombre: item.nombre,
                            datos: null,
                            error: err.message
                        };
                    }
                })
            );

            setMetricas(resultados);

        } catch (err) {
            setError("No se pudieron cargar las métricas: " + err.message);
        } finally {
            setCargando(false);
        }
    }, [torneoSeleccionado]);

    useEffect(() => {
        if (torneoSeleccionado !== "") {
            cargarMetricas();
        }
    }, [torneoSeleccionado, cargarMetricas]);

    // Mostrar los datos de forma genérica
    function mostrarDatos(datos) {
        if (datos === null || datos === undefined) {
            return "Sin datos";
        }

        if (typeof datos !== "object") {
            return String(datos);
        }

        if (Array.isArray(datos)) {
            if (datos.length === 0) {
                return "No hay registros";
            }

            return (
                <div className="metrica-tabla">
                    <table>
                        <thead>
                            <tr>
                                {Object.keys(datos[0]).map((campo) => (
                                    <th key={campo}>{campo.replaceAll("_", " ")}</th>
                                ))}
                            </tr>
                        </thead>

                        <tbody>
                            {datos.map((fila, index) => (
                                <tr key={index}>
                                    {Object.keys(datos[0]).map((campo) => (
                                        <td key={campo}>
                                            {typeof fila[campo] === "object" && fila[campo] !== null
                                                ? JSON.stringify(fila[campo])
                                                : String(fila[campo] ?? "-")}
                                        </td>
                                    ))}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            );
        }

        return (
            <div className="metrica-datos">
                {Object.entries(datos).map(([clave, valor]) => (
                    <p key={clave}>
                        <strong>{clave.replaceAll("_", " ")}:</strong>{" "}
                        {typeof valor === "object" && valor !== null
                            ? JSON.stringify(valor)
                            : String(valor ?? "-")}
                    </p>
                ))}
            </div>
        );
    }

    return (
        <div className="metricas-container">
            <header className="metricas-header">
                <h1>Métricas del torneo</h1>
                <p>Estadísticas e indicadores de rendimiento.</p>
            </header>

            <div className="metricas-filtros">
                <label htmlFor="torneo">Seleccionar torneo:</label>

                <select
                    id="torneo"
                    value={torneoSeleccionado}
                    onChange={(e) => setTorneoSeleccionado(e.target.value)}
                >
                    <option value="">Seleccioná un torneo</option>

                    {torneos.map((torneo) => (
                        <option
                            key={torneo.id_torneo}
                            value={torneo.id_torneo}
                        >
                            {torneo.nombre} - {torneo.anio} (Semestre {torneo.semestre})
                        </option>
                    ))}
                </select>
            </div>

            {error && (
                <p className="metricas-error">{error}</p>
            )}

            {cargando && (
                <p className="metricas-cargando">Cargando métricas...</p>
            )}

            {!cargando && metricas.length > 0 && (
                <div className="metricas-grid">
                    {metricas.map((metrica, index) => (
                        <section className="metrica-card" key={index}>
                            <h2>{metrica.nombre}</h2>

                            {metrica.error ? (
                                <p className="metrica-error">
                                    {metrica.error}
                                </p>
                            ) : (
                                mostrarDatos(metrica.datos)
                            )}
                        </section>
                    ))}
                </div>
            )}

            {!cargando && torneos.length === 0 && !error && (
                <p>No hay torneos disponibles.</p>
            )}
        </div>
    );
}
