<<<<<<< HEAD
import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "./Metricas.css";

const API_URL = "http://127.0.0.1:8000";

const endpoints = [
    { id: "porcentaje_partidos", titulo: "Porcentaje de partidos" },
    { id: "ultima-fecha", titulo: "Partidos de última fecha" },
    { id: "cantidad_sanciones", titulo: "Cantidad de sanciones" },
    { id: "goles_favor", titulo: "Goles a favor" },
    { id: "promedio_equipo", titulo: "Promedio por equipo" },
    { id: "jugadores_sin_plantilla", titulo: "Jugadores sin plantilla" },
    { id: "jugador_facultad_tipo", titulo: "Jugador por facultad y tipo" },
    { id: "goleadores", titulo: "Goleadores" },
    { id: "turnos", titulo: "Turnos más utilizados" },
    { id: "canchas", titulo: "Canchas más usadas" },
    { id: "promedio_goles_torneo", titulo: "Goles por torneo" },
    { id: "promedio_goles_fecha", titulo: "Goles por fecha" },
    { id: "puntos_fair_play", titulo: "Puntos Fair Play" },
    { id: "tabla_torneo", titulo: "Tabla del torneo" },
];

function DatosMetricas({ datos }) {

    if (datos === null || datos === undefined) {
        return <p>Sin datos disponibles.</p>;
    }

    if (Array.isArray(datos)) {

        if (datos.length === 0) {
            return <p>No hay registros.</p>;
        }

        if (datos.every(item => typeof item === "object" && item !== null && !Array.isArray(item))) {

            const columnas = [...new Set(datos.flatMap(item => Object.keys(item)))];

            return (
                <div className="tabla-container">
                    <table>
                        <thead>
                            <tr>
                                {columnas.map(columna => (
                                    <th key={columna}>{columna}</th>
                                ))}
                            </tr>
                        </thead>

                        <tbody>
                            {datos.map((fila, index) => (
                                <tr key={index}>
                                    {columnas.map(columna => (
                                        <td key={columna}>
                                            {mostrarValor(fila[columna])}
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
            <ul>
                {datos.map((item, index) => (
                    <li key={index}>{mostrarValor(item)}</li>
                ))}
            </ul>
        );
    }

    if (typeof datos === "object") {
        return (
            <div className="datos-objeto">
                {Object.entries(datos).map(([clave, valor]) => (
                    <div className="dato" key={clave}>
                        <strong>{clave}:</strong>

                        {typeof valor === "object" && valor !== null ? (
                            <DatosMetricas datos={valor} />
                        ) : (
                            <span>{mostrarValor(valor)}</span>
                        )}
                    </div>
                ))}
            </div>
        );
    }

    return <p className="valor-simple">{mostrarValor(datos)}</p>;
}

function mostrarValor(valor) {
    if (valor === null || valor === undefined) return "N/A";
    if (typeof valor === "boolean") return valor ? "Sí" : "No";
    if (typeof valor === "object") return JSON.stringify(valor);

    return String(valor);
}

export function Metricas() {

    const [metricas, setMetricas] = useState({});
    const [errores, setErrores] = useState({});
    const [cargando, setCargando] = useState(true);

    const cargarMetricas = useCallback(async () => {

    setCargando(true);

    const token = localStorage.getItem("token");

    if (!token) {
        setErrores({ general: "No estás autenticado. Iniciá sesión nuevamente." });
        setCargando(false);
        return;
    }

    const resultados = await Promise.all(
        endpoints.map(async (endpoint) => {

            try {
                const response = await fetch(
                    `${API_URL}/metricas/${endpoint.id}`,
                    {
                        method: "GET",
                        headers: {
                            "Authorization": `Bearer ${token}`
                        }
                    }
                );

                if (response.status === 401) {
                    throw new Error("Sesión vencida o token inválido");
                }

                if (response.status === 403) {
                    throw new Error("No tenés permisos para consultar esta métrica");
                }

                if (!response.ok) {
                    throw new Error(`Error HTTP ${response.status}`);
                }

                const datos = await response.json();

                return {
                    id: endpoint.id,
                    datos: datos,
                    error: null
                };

            } catch (error) {

                return {
                    id: endpoint.id,
                    datos: null,
                    error: error.message
                };
            }
        })
    );

    const nuevosDatos = {};
    const nuevosErrores = {};

    resultados.forEach(resultado => {
        nuevosDatos[resultado.id] = resultado.datos;

        if (resultado.error) {
            nuevosErrores[resultado.id] = resultado.error;
        }
    });

    setMetricas(nuevosDatos);
    setErrores(nuevosErrores);
    setCargando(false);

}, []);

    useEffect(() => {
        cargarMetricas();
    }, [cargarMetricas]);

    return (
        <div className="metricas-page">

            <header className="metricas-header">
                <Link to="/">⬅ Volver</Link>

                <h1>Métricas del torneo</h1>

                <button onClick={cargarMetricas} disabled={cargando}>
                    {cargando ? "Actualizando..." : "↻ Actualizar métricas"}
                </button>
            </header>

            {cargando && Object.keys(metricas).length === 0 ? (

                <p className="mensaje-carga">
                    Cargando métricas...
                </p>

            ) : (

                <div className="metricas-grid">

                    {endpoints.map(endpoint => (

                        <section className="metrica-card" key={endpoint.id}>

                            <h2>{endpoint.titulo}</h2>

                            {errores[endpoint.id] ? (

                                <p className="error">
                                    Error al cargar: {errores[endpoint.id]}
                                </p>

                            ) : (

                                <DatosMetricas datos={metricas[endpoint.id]} />

                            )}

                        </section>

                    ))}

                </div>

            )}

        </div>
    );
=======
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
>>>>>>> e65a8d13e8513362d9f07292a50b70127fdb32d2
}