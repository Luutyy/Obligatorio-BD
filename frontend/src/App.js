
import { BrowserRouter, Routes, Route, Navigate, Outlet } from "react-router-dom";

import "./App.css";

// Páginas principales
import { Inicio } from "./components/Inicio";
import { Login } from "./components/Login/Login";
import { Metricas } from "./components/Metricas";
import { Administracion } from "./components/Administracion";

// Listados
import {
    Jugadores,
    Equipos,
    Fechas,
    Facultades,
    EquiposFacultad
} from "./components/ListadosTorneo";

// Página genérica de detalles
import { PaginaDetalle } from "./components/PaginasAPI";

// Estructura principal de la aplicación
function Layout() {
    return (
        <div className="app">
            <Outlet />
        </div>
    );
}

function App() {
    return (
        <BrowserRouter future={{ v7_startTransition: true }}>
            <Routes>

                {/* Estructura general */}
                <Route path="/" element={<Layout />}>

                    {/* Página inicial */}
                    <Route index element={<Navigate to="/inicio" replace />} />

                    <Route path="inicio" element={<Inicio />} />

                    {/* Autenticación */}
                    <Route path="login" element={<Login />} />

                    {/* Métricas */}
                    <Route path="metricas" element={<Metricas />} />

                    {/* Facultades */}
                    <Route path="facultades" element={<Facultades />} />

                    <Route
                        path="facultades/:id/equipos"
                        element={<EquiposFacultad />}
                    />

                    {/* Jugadores */}
                    <Route path="jugadores" element={<Jugadores />} />

                    <Route
                        path="jugadores/:id"
                        element={
                            <PaginaDetalle
                                titulo="Detalle del jugador"
                                endpoint="/jugadores/:id"
                            />
                        }
                    />

                    {/* Equipos */}
                    <Route path="equipos" element={<Equipos />} />

                    <Route
                        path="equipos/:id"
                        element={
                            <PaginaDetalle
                                titulo="Detalle del equipo"
                                endpoint="/equipos/:id"
                            />
                        }
                    />

                    <Route
                        path="equipos/:id/plantel"
                        element={
                            <PaginaDetalle
                                titulo="Plantel del equipo"
                                endpoint="/equipos/:id/plantel"
                            />
                        }
                    />

                    {/* Fechas y partidos */}
                    <Route path="fechas" element={<Fechas />} />

                    <Route
                        path="partidos/:id"
                        element={
                            <PaginaDetalle
                                titulo="Detalle del partido"
                                endpoint="/partidos/:id"
                            />
                        }
                    />
                    <Route
    path="administracion"
    element={<Administracion />}
/>

                    {/* Complejos */}
                    <Route
                        path="complejos"
                        element={
                            <PaginaDetalle
                                titulo="Complejos"
                                endpoint="/complejos"
                            />
                        }
                    />

                    {/* Torneos */}
                    <Route
                        path="torneos"
                        element={
                            <PaginaDetalle
                                titulo="Torneos"
                                endpoint="/torneos"
                            />
                        }
                    />

                    {/* Sanciones */}
                    <Route
                        path="sanciones"
                        element={
                            <PaginaDetalle
                                titulo="Sanciones"
                                endpoint="/sanciones"
                            />
                        }
                    />

                    {/* Turnos */}
                    <Route
                        path="turnos"
                        element={
                            <PaginaDetalle
                                titulo="Turnos"
                                endpoint="/turnos"
                            />
                        }
                    />

                    {/* Ruta no encontrada */}
                    <Route
                        path="*"
                        element={<Navigate to="/inicio" replace />}
                    />

                </Route>
            </Routes>
        </BrowserRouter>
    );
}

export default App;
