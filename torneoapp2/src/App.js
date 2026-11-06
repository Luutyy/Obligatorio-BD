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
import { Jugadores } from '.components/Jugadores/Jugadores';


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
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
