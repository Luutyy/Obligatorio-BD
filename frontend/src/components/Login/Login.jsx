import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Login.css";

const API_URL = "http://127.0.0.1:8000";

export function Login() {

    const navigate = useNavigate();

    const [correo, setCorreo] = useState("");
    const [contrasena, setContrasena] = useState("");
    const [error, setError] = useState("");
    const [cargando, setCargando] = useState(false);

    async function iniciarSesion(e) {
        e.preventDefault();

        setError("");
        setCargando(true);

        try {
            const response = await fetch(`${API_URL}/login`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    correo: correo,
                    contrasena: contrasena
                })
            });

            const datos = await response.json();

            if (!response.ok) {
                throw new Error(
                    datos.detail || "Error al iniciar sesión"
                );
            }

            // Guardamos el token y el rol
            localStorage.setItem("token", datos.token);
            localStorage.setItem("rol", datos.rol);

            // Redirigimos al inicio
            navigate("/inicio");

        } catch (error) {
            setError(
                error.message === "Failed to fetch"
                    ? "No se pudo conectar con el servidor."
                    : error.message
            );
        } finally {
            setCargando(false);
        }
    }

    return (
        <div className="login-container">

            <form className="login-form" onSubmit={iniciarSesion}>

                <h1>Iniciar sesión</h1>

                <div className="login-campo">
                    <label htmlFor="correo">Correo electrónico</label>

                    <input
                        id="correo"
                        type="email"
                        value={correo}
                        onChange={(e) => setCorreo(e.target.value)}
                        placeholder="Ingrese su correo"
                        required
                    />
                </div>

                <div className="login-campo">
                    <label htmlFor="contrasena">Contraseña</label>

                    <input
                        id="contrasena"
                        type="password"
                        value={contrasena}
                        onChange={(e) => setContrasena(e.target.value)}
                        placeholder="Ingrese su contraseña"
                        required
                    />
                </div>

                {error && (
                    <p className="login-error">{error}</p>
                )}

                <button type="submit" disabled={cargando}>
                    {cargando ? "Ingresando..." : "Ingresar"}
                </button>

            </form>

        </div>
    );
}
