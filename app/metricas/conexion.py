import os
import threading
import mysql.connector

USUARIOS = {
    "administrador": "DB_ADMIN",
    "planillero": "DB_PLANILLERO",
    None: "DB_LECTOR",
}


def get_conexion(rol=None):
    if rol not in USUARIOS:
        raise ValueError(f"Rol desconocido: {rol}")
    prefijo = USUARIOS[rol]
    return mysql.connector.connect(
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        user=os.environ[f"{prefijo}_USER"],
        password=os.environ[f"{prefijo}_PASSWORD"],
        database=os.environ["MYSQL_DATABASE"],
        autocommit=(rol is None),
    )


class _ConexionPublica:

    def __init__(self):
        self._local = threading.local()

    def _conn(self):
        c = getattr(self._local, "conn", None)
        if c is None:
            c = get_conexion(None)
            self._local.conn = c
        else:
            c.ping(reconnect=True, attempts=3, delay=1)
        return c

    def cursor(self, *args, **kwargs):
        return self._conn().cursor(*args, **kwargs)


conexion = _ConexionPublica()