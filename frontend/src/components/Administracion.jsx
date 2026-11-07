import { useCallback, useEffect, useMemo, useState } from "react";
import "./Administracion.css";

const API_URL = (process.env.REACT_APP_API_URL || "http://localhost:8000").replace(/\/+$/, "");

const recursos = [
    {
        id: "jugadores", nombre: "Jugadores", lista: "/jugadores", crear: "/jugadores",
        actualizar: (d) => `/jugadores/${encodeURIComponent(d.ci)}`,
        eliminar: (d) => `/jugadores/${encodeURIComponent(d.ci)}`,
        campos: [
            ["nombre", "Nombre", "text"], ["apellido", "Apellido", "text"],
            ["ci", "Cédula", "text"], ["email", "Correo", "email"],
            ["fecha_nacimiento", "Fecha de nacimiento", "date"],
            ["id_facultad", "ID de facultad", "number"], ["tipo", "Tipo", "text"]
        ]
    },
    {
        id: "equipos", nombre: "Equipos", lista: "/equipos", crear: "/equipo",
        actualizar: (d) => `/equipo/${d.id_equipo}`, eliminar: (d) => `/equipo/${d.id_equipo}`,
        campos: [
            ["nombre", "Nombre", "text"], ["id_torneo", "ID de torneo", "number"],
            ["id_facultad", "ID de facultad", "number"], ["ci_capitan", "CI del capitán", "text"]
        ]
    },
    {
        id: "complejos", nombre: "Complejos", lista: "/complejos", crear: "/complejos",
        actualizar: (d) => `/complejos/${d.id_complejo}`, eliminar: (d) => `/complejos/${d.id_complejo}`,
        campos: [
            ["id_complejo", "ID de complejo", "number"], ["nombre_complejo", "Nombre", "text"],
            ["direccion", "Dirección", "text"], ["departamento", "Departamento", "text"]
        ]
    },
    {
        id: "canchas", nombre: "Canchas", lista: (d) => `/complejos/${d.id_complejo}/canchas`,
        crear: "/canchas",
        actualizar: (d) => `/canchas/${d.id_complejo}/${encodeURIComponent(d.nombre_cancha)}`,
        eliminar: (d) => `/canchas/${d.id_complejo}/${encodeURIComponent(d.nombre_cancha)}`,
        campos: [
            ["nombre_cancha", "Nombre de cancha", "text"], ["id_complejo", "ID de complejo", "number"],
            ["superficie", "Superficie", "text"], ["techada", "¿Techada?", "boolean"]
        ],
        necesitaIdLista: true
    },
    {
        id: "partidos", nombre: "Partidos / fechas", lista: "/partidos", crear: "/partidos",
        actualizar: (d) => `/partidos/${d.id_partido}`, eliminar: (d) => `/partidos/${d.id_partido}`,
        campos: [
            ["id_torneo", "ID de torneo", "number"], ["numero_fecha", "Número de fecha", "number"],
            ["id_equipo_local", "ID equipo local", "number"], ["id_equipo_visitante", "ID equipo visitante", "number"],
            ["dia", "Día", "date"], ["id_turno", "ID de turno", "number"],
            ["nombre_cancha", "Nombre de cancha", "text"], ["id_complejo", "ID de complejo", "number"],
            ["estado", "Estado", "text"]
        ]
    },
    {
        id: "sanciones", nombre: "Sanciones", lista: "/sanciones", crear: "/sanciones",
        actualizar: (d) => `/sanciones/${d.id_sancion}`, eliminar: (d) => `/sanciones/${d.id_sancion}`,
        campos: [
            ["ci_jugador", "CI del jugador", "number"], ["id_torneo", "ID de torneo", "number"],
            ["motivo", "Motivo", "text"], ["numero_fecha_inicio", "Fecha de inicio (número)", "number"],
            ["cantidad_fechas", "Cantidad de fechas", "number"]
        ],
        campoIdManual: ["id_sancion", "ID de sanción"]
    },
    {
        id: "usuarios", nombre: "Usuarios", lista: "/usuarios", crear: "/usuarios",
        campos: [
            ["correo", "Correo", "email"], ["contrasena", "Contraseña", "password"],
            ["rol", "Rol (administrador o planillero)", "text"]
        ]
    },
    {
        id: "planillas", nombre: "Planillas", lista: "/planillas", crear: "/planillas",
        eliminar: (d) => `/planillas/${d.id_partido}/${d.ci_jugador}`,
        campos: [
            ["id_partido", "ID de partido", "number"], ["ci_jugador", "CI del jugador", "number"],
            ["id_equipo", "ID de equipo", "number"]
        ]
    },
    {
        id: "vinculaciones", nombre: "Jugadores en equipos", lista: "/equipo-jugador-torneo",
        crear: "/equipo-jugador-torneo",
        actualizar: (d) => `/equipo-jugador-torneo/${d.id_torneo}/${d.ci_jugador}`,
        eliminar: (d) => `/equipo-jugador-torneo/${d.id_torneo}/${d.ci_jugador}`,
        campos: [
            ["id_equipo", "ID de equipo", "number"], ["ci_jugador", "CI del jugador", "number"],
            ["id_torneo", "ID de torneo", "number"], ["numero_camiseta", "Número de camiseta", "number"]
        ]
    },
    {
        id: "goles", nombre: "Goles", crear: "/goles",
        actualizar: (d) => `/goles/${d.id_gol}`, eliminar: (d) => `/goles/${d.id_gol}`,
        campos: [
            ["id_partido", "ID de partido", "number"], ["ci_jugador", "CI del jugador", "number"],
            ["minuto", "Minuto", "number"], ["autogol", "¿Autogol?", "boolean"]
        ],
        campoIdManual: ["id_gol", "ID de gol"]
    },
    {
        id: "tarjetas", nombre: "Tarjetas", crear: "/tarjetas",
        actualizar: (d) => `/tarjetas/${d.id_tarjeta}`, eliminar: (d) => `/tarjetas/${d.id_tarjeta}`,
        campos: [
            ["id_partido", "ID de partido", "number"], ["ci_jugador", "CI del jugador", "text"],
            ["minuto", "Minuto", "number"], ["color", "Color (amarilla/roja)", "text"]
        ],
        campoIdManual: ["id_tarjeta", "ID de tarjeta"]
    },
    { id: "facultades", nombre: "Facultades (solo consulta)", lista: "/facultades", soloLectura: true },
    { id: "torneos", nombre: "Torneos (solo consulta)", lista: "/torneos", soloLectura: true },
    { id: "turnos", nombre: "Turnos (solo consulta)", lista: "/turnos", soloLectura: true }
];

async function api(endpoint, method = "GET", body) {
    const token = localStorage.getItem("token");
    const response = await fetch(`${API_URL}${endpoint}`, {
        method,
        headers: {
            ...(body !== undefined ? { "Content-Type": "application/json" } : {}),
            ...(token ? { Authorization: `Bearer ${token}` } : {})
        },
        ...(body !== undefined ? { body: JSON.stringify(body) } : {})
    });

    const texto = await response.text();
    let datos = null;
    try { datos = texto ? JSON.parse(texto) : null; }
    catch { datos = texto; }

    if (!response.ok) {
        const detalle = typeof datos === "string" ? datos : JSON.stringify(datos);
        throw new Error(`HTTP ${response.status}: ${detalle || response.statusText}`);
    }
    return datos;
}

const valorInicial = (tipo) => tipo === "boolean" ? false : "";

export function Administracion() {
    const [recursoId, setRecursoId] = useState("jugadores");
    const [registros, setRegistros] = useState([]);
    const [formulario, setFormulario] = useState({});
    const [idLista, setIdLista] = useState("");
    const [modo, setModo] = useState("crear");
    const [registroSeleccionado, setRegistroSeleccionado] = useState(null);
    const [cargando, setCargando] = useState(false);
    const [guardando, setGuardando] = useState(false);
    const [mensaje, setMensaje] = useState("");
    const [error, setError] = useState("");

    const recurso = useMemo(
        () => recursos.find((r) => r.id === recursoId) || recursos[0],
        [recursoId]
    );

    const cargarRegistros = useCallback(async () => {
        if (!recurso.lista) {
            setRegistros([]);
            return;
        }
        if (recurso.necesitaIdLista && !idLista) {
            setRegistros([]);
            return;
        }
        setCargando(true);
        setError("");
        try {
            const endpoint = typeof recurso.lista === "function"
                ? recurso.lista({ id_complejo: idLista })
                : recurso.lista;
            const datos = await api(endpoint);
            setRegistros(Array.isArray(datos) ? datos : datos ? [datos] : []);
        } catch (e) {
            setError(`No se pudo cargar ${recurso.nombre}: ${e.message}`);
            setRegistros([]);
        } finally {
            setCargando(false);
        }
    }, [recurso, idLista]);

    useEffect(() => {
        setFormulario({});
        setRegistroSeleccionado(null);
        setModo("crear");
        setMensaje("");
        setError("");
        setRegistros([]);
        if (!recurso.necesitaIdLista) setIdLista("");
    }, [recursoId, recurso]);

    useEffect(() => {
        if (recurso.lista && (!recurso.necesitaIdLista || idLista)) cargarRegistros();
    }, [cargarRegistros, recurso.lista, recurso.necesitaIdLista, idLista]);

    function nuevoFormulario() {
        const inicial = {};
        (recurso.campos || []).forEach(([campo, , tipo]) => {
            inicial[campo] = valorInicial(tipo);
        });
        if (recurso.campoIdManual) inicial[recurso.campoIdManual[0]] = "";
        setFormulario(inicial);
        setRegistroSeleccionado(null);
        setModo("crear");
        setMensaje("");
        setError("");
    }

    function seleccionarParaEditar(registro) {
        const copia = {};
        (recurso.campos || []).forEach(([campo, , tipo]) => {
            copia[campo] = registro[campo] ?? valorInicial(tipo);
        });
        if (recurso.campoIdManual) {
            copia[recurso.campoIdManual[0]] = registro[recurso.campoIdManual[0]] ?? "";
        }
        // Las APIs pueden devolver la clave primaria junto con el resto de los campos.
        if (recurso.id === "equipos") copia.id_equipo = registro.id_equipo;
        if (recurso.id === "partidos") copia.id_partido = registro.id_partido;
        if (recurso.id === "complejos") copia.id_complejo = registro.id_complejo;
        setFormulario(copia);
        setRegistroSeleccionado(registro);
        setModo("editar");
        setMensaje("");
        setError("");
    }

    function cambiarCampo(campo, valor, tipo) {
        setFormulario((actual) => ({
            ...actual,
            [campo]: tipo === "number" ? (valor === "" ? "" : Number(valor)) : valor
        }));
    }

    async function guardar(e) {
        e.preventDefault();
        setGuardando(true);
        setMensaje("");
        setError("");
        try {
            const payload = {};
            (recurso.campos || []).forEach(([campo, , tipo]) => {
                payload[campo] = tipo === "number" ? Number(formulario[campo]) : formulario[campo];
            });

            if (modo === "editar" && recurso.campoIdManual) {
                // El ID manual identifica el registro; no forma parte del cuerpo del modelo.
            }

            let endpoint;
            let method;
            if (modo === "editar") {
                if (!recurso.actualizar) throw new Error("Esta entidad no tiene endpoint PUT.");
                endpoint = recurso.actualizar({ ...formulario, ...registroSeleccionado });
                method = "PUT";
            } else {
                if (!recurso.crear) throw new Error("Esta entidad no tiene endpoint POST.");
                endpoint = recurso.crear;
                method = "POST";
            }

            await api(endpoint, method, payload);
            setMensaje(modo === "editar" ? "Registro modificado correctamente." : "Registro creado correctamente.");
            await cargarRegistros();
            if (modo === "crear") nuevoFormulario();
        } catch (e2) {
            setError(e2.message);
        } finally {
            setGuardando(false);
        }
    }

    async function eliminar(registro) {
        if (!recurso.eliminar) return;
        const confirmado = window.confirm("¿Seguro que querés eliminar este registro? Esta acción no se puede deshacer.");
        if (!confirmado) return;

        try {
            await api(recurso.eliminar(registro), "DELETE");
            setMensaje("Registro eliminado correctamente.");
            setError("");
            if (registroSeleccionado === registro) nuevoFormulario();
            await cargarRegistros();
        } catch (e) {
            setError(e.message);
        }
    }

    async function accionPorId(e, accion) {
        e.preventDefault();
        setError("");
        setMensaje("");
        try {
            const datos = { ...formulario };
            if (recurso.campoIdManual) {
                const [id] = recurso.campoIdManual;
                if (!datos[id]) throw new Error(`Ingresá ${id}.`);
            }
            if (accion === "eliminar") {
                if (!window.confirm("¿Seguro que querés eliminar este registro?")) return;
                await api(recurso.eliminar(datos), "DELETE");
                setMensaje("Registro eliminado correctamente.");
            } else {
                await api(recurso.actualizar(datos), "PUT", Object.fromEntries(
                    recurso.campos.map(([campo, , tipo]) => [
                        campo, tipo === "number" ? Number(datos[campo]) : datos[campo]
                    ])
                ));
                setMensaje("Registro modificado correctamente.");
            }
            await cargarRegistros();
        } catch (e2) {
            setError(e2.message);
        }
    }

    return (
        <main className="admin-db">
            <header className="admin-db-header">
                <div>
                    <p className="admin-db-eyebrow">TORNEO · ADMINISTRACIÓN</p>
                    <h1>Administrar base de datos</h1>
                    <p>Crear, consultar, modificar y eliminar registros del sistema.</p>
                </div>
            </header>

            <section className="admin-db-toolbar">
                <label htmlFor="recurso-admin">Sección</label>
                <select id="recurso-admin" value={recursoId} onChange={(e) => setRecursoId(e.target.value)}>
                    {recursos.map((r) => <option key={r.id} value={r.id}>{r.nombre}</option>)}
                </select>
                {recurso.lista && (
                    <button type="button" className="admin-btn admin-btn-secondary" onClick={cargarRegistros}>
                        Actualizar listado
                    </button>
                )}
            </section>

            {recurso.necesitaIdLista && (
                <section className="admin-db-panel admin-db-filter">
                    <label htmlFor="id-complejo-lista">ID del complejo para consultar sus canchas</label>
                    <input id="id-complejo-lista" type="number" value={idLista}
                        onChange={(e) => setIdLista(e.target.value)} placeholder="Ej. 1" />
                </section>
            )}

            {mensaje && <div className="admin-alert admin-alert-success">{mensaje}</div>}
            {error && <div className="admin-alert admin-alert-error">{error}</div>}

            <div className="admin-db-layout">
                <section className="admin-db-panel admin-db-list">
                    <div className="admin-panel-heading">
                        <div>
                            <h2>{recurso.nombre}</h2>
                            <span>{registros.length} registro(s)</span>
                        </div>
                    </div>

                    {!recurso.lista && (
                        <p className="admin-empty">
                            El Swagger no publica un GET de listado para esta entidad. Podés registrar,
                            modificar o eliminar indicando el identificador correspondiente.
                        </p>
                    )}
                    {cargando && <p>Cargando registros...</p>}
                    {!cargando && recurso.lista && registros.length === 0 && (
                        <p className="admin-empty">No hay registros para mostrar.</p>
                    )}

                    <div className="admin-records">
                        {registros.map((registro, index) => (
                            <article className="admin-record" key={registro.id ?? registro.ci ?? registro.id_equipo ?? registro.id_partido ?? index}>
                                <pre>{JSON.stringify(registro, null, 2)}</pre>
                                <div className="admin-record-actions">
                                    {recurso.actualizar && (
                                        <button type="button" className="admin-btn admin-btn-secondary"
                                            onClick={() => seleccionarParaEditar(registro)}>Editar</button>
                                    )}
                                    {recurso.eliminar && (
                                        <button type="button" className="admin-btn admin-btn-danger"
                                            onClick={() => eliminar(registro)}>Eliminar</button>
                                    )}
                                </div>
                            </article>
                        ))}
                    </div>
                </section>

                <section className="admin-db-panel admin-db-form-panel">
                    <div className="admin-panel-heading">
                        <div>
                            <h2>{modo === "editar" ? "Modificar registro" : "Crear registro"}</h2>
                            <span>{recurso.nombre}</span>
                        </div>
                        {modo === "editar" && (
                            <button type="button" className="admin-btn admin-btn-secondary" onClick={nuevoFormulario}>
                                Cancelar edición
                            </button>
                        )}
                    </div>

                    {recurso.soloLectura ? (
                        <p className="admin-empty">Esta entidad solo tiene operaciones GET en el backend.</p>
                    ) : (
                        <form onSubmit={guardar}>
                            {recurso.campoIdManual && (
                                <div className="admin-field">
                                    <label htmlFor={`campo-${recurso.campoIdManual[0]}`}>{recurso.campoIdManual[1]}</label>
                                    <input id={`campo-${recurso.campoIdManual[0]}`} type="number"
                                        value={formulario[recurso.campoIdManual[0]] ?? ""}
                                        onChange={(e) => cambiarCampo(recurso.campoIdManual[0], e.target.value, "number")}
                                        required={modo === "editar"} />
                                </div>
                            )}

                            {(recurso.campos || []).map(([campo, etiqueta, tipo]) => {
                                const esClaveSoloLectura = modo === "editar" &&
                                    ((recurso.id === "jugadores" && campo === "ci") ||
                                     (recurso.id === "complejos" && campo === "id_complejo"));
                                return (
                                    <div className="admin-field" key={campo}>
                                        <label htmlFor={`campo-${campo}`}>{etiqueta}</label>
                                        {tipo === "boolean" ? (
                                            <label className="admin-checkbox">
                                                <input type="checkbox" checked={Boolean(formulario[campo])}
                                                    onChange={(e) => cambiarCampo(campo, e.target.checked, tipo)} />
                                                Sí
                                            </label>
                                        ) : (
                                            <input id={`campo-${campo}`} type={tipo}
                                                value={formulario[campo] ?? ""}
                                                onChange={(e) => cambiarCampo(campo, e.target.value, tipo)}
                                                required={!esClaveSoloLectura}
                                                readOnly={esClaveSoloLectura}
                                            />
                                        )}
                                    </div>
                                );
                            })}

                            <div className="admin-form-actions">
                                <button className="admin-btn admin-btn-primary" type="submit" disabled={guardando}>
                                    {guardando ? "Guardando..." : modo === "editar" ? "Guardar cambios" : "Crear registro"}
                                </button>
                                {modo === "crear" && recurso.actualizar && recurso.campoIdManual && (
                                    <button className="admin-btn admin-btn-secondary" type="button"
                                        onClick={(e) => accionPorId(e, "modificar")}>Modificar por ID</button>
                                )}
                                {modo === "crear" && recurso.eliminar && recurso.campoIdManual && (
                                    <button className="admin-btn admin-btn-danger" type="button"
                                        onClick={(e) => accionPorId(e, "eliminar")}>Eliminar por ID</button>
                                )}
                            </div>
                        </form>
                    )}
                </section>
            </div>
        </main>
    );
}
