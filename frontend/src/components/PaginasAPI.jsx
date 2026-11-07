
import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import "./PaginasAPI.css";

const API_URL = (
    process.env.REACT_APP_API_URL || "http://localhost:8000"
).replace(/\/+$/, "");

// Componente que muestra cualquier respuesta JSON
export function MostrarDatos({ datos }) {

    if (datos === null || datos === undefined) {
        return <p>No hay datos disponibles.</p>;
    }

    if (Array.isArray(datos)) {

        if (datos.length === 0) {
            return <p>No hay registros.</p>;
        }

        if (datos.every(item =>
            typeof item === "object" &&
            item !== null &&
            !Array.isArray(item)
        )) {

            const columnas = [
                ...new Set(datos.flatMap(item => Object.keys(item)))
            ];

            return (
                <div className="api-tabla-container">
                    <table className="api-tabla">
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
                                            <MostrarDatos datos={fila[columna]} />
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
                    <li key={index}>
                        <MostrarDatos datos={item} />
                    </li>
                ))}
            </ul>
        );
    }

    if (typeof datos === "object") {

        return (
            <div className="api-objeto">
                {Object.entries(datos).map(([clave, valor]) => (
                    <div className="api-dato" key={clave}>
                        <strong>{clave.replaceAll("_", " ")}:</strong>

                        <MostrarDatos datos={valor} />
                    </div>
                ))}
            </div>
        );
    }

    if (typeof datos === "boolean") {
        return <span>{datos ? "Sí" : "No"}</span>;
    }

    return <span>{String(datos)}</span>;
}

// Componente para mostrar una página que consulta un endpoint
export function PaginaAPI({ titulo, endpoint }) {

    const [datos, setDatos] = useState(null);
    const [cargando, setCargando] = useState(true);
    const [error, setError] = useState("");

    async function cargarDatos() {

        setCargando(true);
        setError("");

        try {

            const token = localStorage.getItem("token");

            const response = await fetch(`${API_URL}${endpoint}`, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });

            if (response.status === 401) {
                throw new Error("Sesión vencida o no autenticada.");
            }

            if (response.status === 403) {
                throw new Error("No tenés permisos para acceder a esta información.");
            }

            if (!response.ok) {
                throw new Error(`Error HTTP ${response.status}`);
            }

            const resultado = await response.json();

            setDatos(resultado);

        } catch (error) {
            setError(error.message);
        } finally {
            setCargando(false);
        }
    }

    useEffect(() => {
        cargarDatos();
    }, [endpoint]);

    return (
        <div className="api-pagina">

            <header className="api-header">
                <Link to="/inicio">⬅ Volver al inicio</Link>
                <h1>{titulo}</h1>
            </header>

            <main className="api-contenido">

                {cargando && <p>Cargando información...</p>}

                {error && (
                    <div className="api-error">
                        {error}
                    </div>
                )}

                {!cargando && !error && (
                    <div className="api-card">
                        <MostrarDatos datos={datos} />
                    </div>
                )}

                <button
                    className="api-actualizar"
                    onClick={cargarDatos}
                    disabled={cargando}
                >
                    Actualizar información
                </button>

            </main>

        </div>
    );
}

// Componente para endpoints que necesitan un parámetro
export function PaginaDetalle({ titulo, endpoint }) {

    const parametros = useParams();

    const endpointFinal = endpoint.replace(
        ":id",
        encodeURIComponent(parametros.id)
    );

    return (
        <PaginaAPI
            titulo={titulo}
            endpoint={endpointFinal}
        />
    );
}
