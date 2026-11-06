import {
  BrowserRouter,
  Navigate,
  Outlet,
  Route,
  Routes,
} from 'react-router-dom';
import styles from './App.css';
import { Inicio } from './components/Inicio';
import { Equipos } from './components/Equipos/Equipos';
import { Facultades } from './components/Equipos/Facultades';
import { Fechas } from './components/Fechas/Fechas';
import { Metricas } from './components/Metricas';
import { Jugadores } from './components/Jugadores/Jugadores';
import { Login } from "./components/Login/Login";
import {
    PaginaAPI,
    PaginaDetalle
} from "./components/PaginasAPI";


export default function App() {

  return (
    <BrowserRouter future={{ v7_startTransition: true }}>
      <Routes>
        <Route
          path="/"
          element={(
            <div className={styles.app}>
              <Outlet />
            </div>
          )}
        >
          <Route index element={<Navigate to="/Inicio" replace />} />
          <Route path="Inicio" element={<Inicio />} />
          <Route path="Equipos" element={<Equipos />} />
          <Route path="Facultades" element={<Facultades />} />
          <Route path="Fechas" element={<Fechas />} />
          <Route path="Metricas" element={<Metricas />} />
          <Route path="Jugadores" element={<Jugadores />} />
          <Route path="login" element={<Login />} />
          
{/* LISTADOS PRINCIPALES */}

<Route
    path="facultades"
    element={<PaginaAPI titulo="Facultades" endpoint="/facultades" />}
/>

<Route
    path="fechas"
    element={<PaginaAPI titulo="Fechas y partidos" endpoint="/partidos" />}
/>

<Route
    path="jugadores"
    element={<PaginaAPI titulo="Jugadores" endpoint="/jugadores" />}
/>

<Route
    path="equipos"
    element={<PaginaAPI titulo="Equipos" endpoint="/equipos" />}
/>

<Route
    path="torneos"
    element={<PaginaAPI titulo="Torneos" endpoint="/torneos" />}
/>

<Route
    path="complejos"
    element={<PaginaAPI titulo="Complejos" endpoint="/complejos" />}
/>

<Route
    path="sanciones"
    element={<PaginaAPI titulo="Sanciones" endpoint="/sanciones" />}
/>

<Route
    path="turnos"
    element={<PaginaAPI titulo="Turnos" endpoint="/turnos" />}
/>

{/* DETALLES DE JUGADORES */}

<Route
    path="jugadores/:id"
    element={<PaginaDetalle titulo="Detalle del jugador" endpoint="/jugadores/:id" />}
/>

{/* DETALLES DE EQUIPOS */}

<Route
    path="equipos/:id"
    element={<PaginaDetalle titulo="Detalle del equipo" endpoint="/equipos/:id" />}
/>

<Route
    path="equipos/:id/plantel"
    element={<PaginaDetalle titulo="Plantel del equipo" endpoint="/equipos/:id/plantel" />}
/>

{/* DETALLES DE TORNEOS */}

<Route
    path="torneos/:id"
    element={<PaginaDetalle titulo="Detalle del torneo" endpoint="/torneos/:id" />}
/>

<Route
    path="torneos/:id/jugadores-disponibles"
    element={<PaginaDetalle titulo="Jugadores disponibles" endpoint="/torneos/:id/jugadores-disponibles" />}
/>

{/* DETALLES DE COMPLEJOS */}

<Route
    path="complejos/:id"
    element={<PaginaDetalle titulo="Detalle del complejo" endpoint="/complejos/:id" />}
/>

<Route
    path="complejos/:id/canchas"
    element={<PaginaDetalle titulo="Canchas del complejo" endpoint="/complejos/:id/canchas" />}
/>

<Route
    path="complejos/:id/canchas/:nombre"
    element={<PaginaDetalle titulo="Detalle de la cancha" endpoint="/complejos/:id/canchas/:nombre" />}
/>

{/* DETALLES DE PARTIDOS */}

<Route
    path="partidos"
    element={<PaginaAPI titulo="Partidos" endpoint="/partidos" />}
/>

<Route
    path="partidos/:id"
    element={<PaginaDetalle titulo="Detalle del partido" endpoint="/partidos/:id" />}
/>

<Route
    path="partidos/:id/planilla"
    element={<PaginaDetalle titulo="Planilla del partido" endpoint="/partidos/:id/planilla" />}
/>

<Route
    path="partidos/:id/jugadores-habilitados"
    element={<PaginaDetalle titulo="Jugadores habilitados" endpoint="/partidos/:id/jugadores-habilitados" />}
/>

<Route
    path="partidos/:id/goles"
    element={<PaginaDetalle titulo="Goles del partido" endpoint="/partidos/:id/goles" />}
/>

<Route
    path="partidos/:id/tarjetas"
    element={<PaginaDetalle titulo="Tarjetas del partido" endpoint="/partidos/:id/tarjetas" />}
/>

<Route
    path="partidos/:id/resultado"
    element={<PaginaDetalle titulo="Resultado del partido" endpoint="/partidos/:id/resultado" />}
/>

{/* DETALLES DE SANCIONES */}

<Route
    path="sanciones/:id"
    element={<PaginaDetalle titulo="Detalle de la sanción" endpoint="/sanciones/:id" />}
/>

        </Route>
      </Routes>
    </BrowserRouter>
  );
}
