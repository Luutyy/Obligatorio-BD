DROP DATABASE IF EXISTS torneo;
CREATE DATABASE torneo
USE torneo;
CREATE TABLE login (
    correo VARCHAR(45) NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    rol ENUM('administrador', 'planillero') NOT NULL,
    PRIMARY KEY (correo)
);

CREATE TABLE facultad (
    id_facultad INT AUTO_INCREMENT,
    nombre VARCHAR(45) NOT NULL,
    PRIMARY KEY (id_facultad)
);

CREATE TABLE torneo (
    id_torneo INT AUTO_INCREMENT,
    nombre VARCHAR(30) NOT NULL,
    anio INT NOT NULL,
    semestre ENUM('1','2') NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    estado ENUM('inscripcion', 'en curso', 'finalizado') NOT NULL,
    PRIMARY KEY (id_torneo)
);

CREATE TABLE complejo (
    id_complejo INT NOT NULL,
    nombre_complejo VARCHAR(30) NOT NULL,
    direccion VARCHAR(60) NOT NULL,
    departamento VARCHAR(30) NOT NULL,
    PRIMARY KEY (id_complejo)
);

CREATE TABLE turno (
    id_turno INT NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    PRIMARY KEY (id_turno)
);

CREATE TABLE jugador (
    ci INT NOT NULL,
    nombre VARCHAR(30) NOT NULL,
    apellido VARCHAR(40) NOT NULL,
    email VARCHAR(60) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    id_facultad INT NOT NULL,
    tipo ENUM('grado','posgrado','docente','funcionario') NOT NULL,
    PRIMARY KEY (ci),
    FOREIGN KEY (id_facultad) REFERENCES facultad(id_facultad)
);

CREATE TABLE equipo (
    id_equipo INT AUTO_INCREMENT,
    nombre VARCHAR(30) NOT NULL,
    id_torneo INT NOT NULL,
    id_facultad INT NOT NULL,
    ci_capitan INT NOT NULL,
    PRIMARY KEY (id_equipo),
    FOREIGN KEY (id_torneo) REFERENCES torneo(id_torneo),
    FOREIGN KEY (id_facultad) REFERENCES facultad(id_facultad),
    FOREIGN KEY (ci_capitan) REFERENCES jugador(ci)
);

CREATE TABLE equipo_jugador_torneo (
    id_equipo INT NOT NULL,
    ci_jugador INT NOT NULL,
    id_torneo INT NOT NULL,
    numero_camiseta INT NOT NULL,
    PRIMARY KEY (ci_jugador, id_torneo),
    FOREIGN KEY (id_equipo) REFERENCES equipo(id_equipo),
    FOREIGN KEY (ci_jugador) REFERENCES jugador(ci),
    FOREIGN KEY (id_torneo) REFERENCES torneo(id_torneo)
);

CREATE TABLE cancha (
    nombre_cancha VARCHAR(30) NOT NULL,
    id_complejo INT NOT NULL,
    superficie ENUM('sintético', 'parquet') NOT NULL,
    techada BOOLEAN NOT NULL,
    PRIMARY KEY (nombre_cancha, id_complejo),
    FOREIGN KEY (id_complejo) REFERENCES complejo(id_complejo)
);

CREATE TABLE partido (
    id_partido INT AUTO_INCREMENT,
    id_torneo INT NOT NULL,
    numero_fecha INT NOT NULL,
    id_equipo_local INT NOT NULL,
    id_equipo_visitante INT NOT NULL,
    dia DATE NOT NULL,
    id_turno INT NOT NULL,
    nombre_cancha VARCHAR(30) NOT NULL,
    id_complejo INT NOT NULL,
    estado ENUM('programado','jugado','postergado','cancelado') NOT NULL,
    PRIMARY KEY (id_partido),
    FOREIGN KEY (id_torneo) REFERENCES torneo(id_torneo),
    FOREIGN KEY (id_equipo_local) REFERENCES equipo(id_equipo),
    FOREIGN KEY (id_equipo_visitante) REFERENCES equipo(id_equipo),
    FOREIGN KEY (id_turno) REFERENCES turno(id_turno),
    FOREIGN KEY (nombre_cancha, id_complejo)
        REFERENCES cancha(nombre_cancha, id_complejo)
);

CREATE TABLE planilla_partido (
    id_partido INT NOT NULL,
    ci_jugador INT NOT NULL,
    id_equipo INT NOT NULL,
    PRIMARY KEY (id_partido, ci_jugador),
    FOREIGN KEY (id_partido) REFERENCES partido(id_partido),
    FOREIGN KEY (ci_jugador) REFERENCES jugador(ci),
    FOREIGN KEY (id_equipo) REFERENCES equipo(id_equipo)
);

CREATE TABLE gol (
    id_gol INT NOT NULL,
    id_partido INT NOT NULL,
    ci_jugador INT NOT NULL,
    minuto INT NOT NULL,
    autogol BOOLEAN NOT NULL,
    PRIMARY KEY (id_gol),
    FOREIGN KEY (id_partido) REFERENCES partido(id_partido),
    FOREIGN KEY (ci_jugador) REFERENCES jugador(ci)
);

CREATE TABLE sancion_jugador (
    id_sancion INT NOT NULL,
    ci_jugador INT NOT NULL,
    id_torneo INT NOT NULL,
    motivo ENUM('roja', 'acumulacion de amarillas', 'disciplinaria') NOT NULL,
    fecha_inicio DATETIME NOT NULL,
    cantidad_fechas INT NOT NULL,
    PRIMARY KEY (id_sancion),
    FOREIGN KEY (ci_jugador) REFERENCES jugador(ci),
    FOREIGN KEY (id_torneo) REFERENCES torneo(id_torneo)
);

CREATE TABLE tarjeta (
    id_tarjeta INT AUTO_INCREMENT,
    id_partido INT NOT NULL,
    ci_jugador INT NOT NULL,
    minuto INT NOT NULL,
    color ENUM('amarilla','roja') NOT NULL,
    PRIMARY KEY (id_tarjeta),
    FOREIGN KEY (id_partido) REFERENCES partido(id_partido),
    FOREIGN KEY (ci_jugador) REFERENCES jugador(ci)
);


INSERT INTO facultad (id_facultad, nombre) VALUES
(1, 'Facultad de Ingenieria'),
(2, 'Facultad de Ciencias Empresariales');

INSERT INTO torneo (id_torneo, nombre, anio, semestre, fecha_inicio, fecha_fin, estado) VALUES
(1, 'Copa Universitaria', 2026, '2', '2026-11-01', '2026-11-30', 'en curso');

INSERT INTO login (correo, contrasena, rol) VALUES
('admin@ucu.edu.uy', 'admin123', 'administrador'),
('planillero1@ucu.edu.uy', 'planilla123', 'planillero'),
('planillero2@ucu.edu.uy', 'planilla456', 'planillero');

INSERT INTO jugador (ci, nombre, apellido, email, fecha_nacimiento, id_facultad, tipo) VALUES
(101, 'Juan', 'Perez', 'juan@gmail.com', '2002-03-10', 1, 'grado'),
(102, 'Lucas', 'Rodriguez', 'lucas@gmail.com', '2001-05-15', 1, 'grado'),
(103, 'Mateo', 'Gonzalez', 'mateo@gmail.com', '2000-08-20', 1, 'grado'),
(104, 'Santiago', 'Fernandez', 'santi@gmail.com', '2002-11-02', 1, 'grado'),
(105, 'Martin', 'Lopez', 'martin@gmail.com', '2001-01-12', 1, 'grado'),
(106, 'Nicolas', 'Silva', 'nico@gmail.com', '2000-06-25', 1, 'grado'),
(107, 'Pedro', 'Martinez', 'pedro@gmail.com', '2001-04-12', 2, 'grado'),
(108, 'Diego', 'Garcia', 'diego@gmail.com', '2002-07-18', 2, 'grado'),
(109, 'Federico', 'Suarez', 'fede@gmail.com', '2000-09-22', 2, 'grado'),
(110, 'Agustin', 'Torres', 'agus@gmail.com', '2001-12-05', 2, 'grado'),
(111, 'Bruno', 'Diaz', 'bruno@gmail.com', '2002-02-14', 2, 'grado'),
(112, 'Tomas', 'Romero', 'tomas@gmail.com', '2000-10-30', 2, 'grado'),
(113, 'Andres', 'Alonso', 'andres@gmail.com', '2001-03-19', 1, 'grado'),
(114, 'Facundo', 'Castro', 'facu@gmail.com', '2002-06-21', 1, 'grado'),
(115, 'Gabriel', 'Mendez', 'gabriel@gmail.com', '2000-12-11', 1, 'grado'),
(116, 'Ignacio', 'Vazquez', 'ignacio@gmail.com', '2001-08-08', 1, 'grado'),
(117, 'Joaquin', 'Ramos', 'joaquin@gmail.com', '2002-01-17', 1, 'grado'),
(118, 'Franco', 'Pereira', 'franco@gmail.com', '2000-05-09', 1, 'grado'),
(119, 'Emiliano', 'Acosta', 'emi@gmail.com', '2001-02-25', 2, 'grado'),
(120, 'Matias', 'Benitez', 'matias@gmail.com', '2002-04-13', 2, 'grado'),
(121, 'Sebastian', 'Cabrera', 'seba@gmail.com', '2000-07-07', 2, 'grado'),
(122, 'Maximiliano', 'Duarte', 'maxi@gmail.com', '2001-10-16', 2, 'grado'),
(123, 'Valentin', 'Etcheverry', 'valen@gmail.com', '2002-09-03', 2, 'grado'),
(124, 'Benjamin', 'Farias', 'benja@gmail.com', '2000-11-28', 2, 'grado');

INSERT INTO complejo (id_complejo, nombre_complejo, direccion, departamento) VALUES
(1, 'Complejo Central', 'Av. Italia 1234', 'Montevideo'),
(2, 'Complejo Deportivo Norte', 'Av. Rivera 2500', 'Montevideo');

INSERT INTO cancha (nombre_cancha, id_complejo, superficie, techada) VALUES
('Cancha 1', 1, 'sintético', TRUE),
('Cancha 2', 1, 'parquet', TRUE),
('Cancha 1', 2, 'sintético', FALSE),
('Cancha 2', 2, 'sintético', TRUE);

INSERT INTO turno (id_turno, hora_inicio, hora_fin) VALUES
(1, '18:00:00', '19:00:00'),
(2, '19:00:00', '20:00:00'),
(3, '20:00:00', '21:00:00'),
(4, '21:00:00', '22:00:00'),
(5, '22:00:00', '23:00:00');

INSERT INTO equipo (id_equipo, nombre, id_torneo, id_facultad, ci_capitan) VALUES
(1, 'Los Ingenieros', 1, 1, 101),
(2, 'Los Empresarios', 1, 2, 107),
(3, 'Los Programadores', 1, 1, 113),
(4, 'Los Contadores', 1, 2, 119);

-- Planteles (se habilitaron los INSERT que estaban comentados)
INSERT INTO equipo_jugador_torneo (id_equipo, ci_jugador, id_torneo, numero_camiseta) VALUES
(1, 101, 1, 1), (1, 102, 1, 2), (1, 103, 1, 3), (1, 104, 1, 4), (1, 105, 1, 5), (1, 106, 1, 6),
(2, 107, 1, 1), (2, 108, 1, 2), (2, 109, 1, 3), (2, 110, 1, 4), (2, 111, 1, 5), (2, 112, 1, 6),
(3, 113, 1, 1), (3, 114, 1, 2), (3, 115, 1, 3), (3, 116, 1, 4), (3, 117, 1, 5), (3, 118, 1, 6),
(4, 119, 1, 1), (4, 120, 1, 2), (4, 121, 1, 3), (4, 122, 1, 4), (4, 123, 1, 5), (4, 124, 1, 6);

INSERT INTO partido (id_partido, id_torneo, numero_fecha, id_equipo_local, id_equipo_visitante, dia, id_turno, nombre_cancha, id_complejo, estado) VALUES
(1, 1, 1, 1, 2, '2026-11-10', 1, 'Cancha 1', 1, 'jugado'),
(2, 1, 1, 3, 4, '2026-11-10', 1, 'Cancha 1', 2, 'programado'),
(3, 1, 2, 1, 3, '2026-11-12', 2, 'Cancha 1', 1, 'programado'),
(4, 1, 2, 2, 4, '2026-11-12', 2, 'Cancha 1', 2, 'programado'),
(5, 1, 3, 1, 4, '2026-11-14', 3, 'Cancha 2', 1, 'programado'),
(6, 1, 3, 2, 3, '2026-11-14', 3, 'Cancha 2', 2, 'programado');

INSERT INTO sancion_jugador (id_sancion, ci_jugador, id_torneo, motivo, fecha_inicio, cantidad_fechas) VALUES
(1, 106, 1, 'acumulacion de amarillas', '2026-11-01 00:00:00', 3);

INSERT INTO gol (id_gol, id_partido, ci_jugador, minuto, autogol) VALUES
(1, 1, 101, 10, FALSE),
(2, 1, 107, 15, FALSE),
(3, 1, 102, 25, FALSE),
(4, 1, 108, 32, FALSE),
(5, 1, 103, 40, TRUE),
(6, 2, 113, 12, FALSE),
(7, 2, 120, 30, FALSE);

INSERT INTO tarjeta (id_tarjeta, id_partido, ci_jugador, minuto, color) VALUES
(1, 1, 102, 18, 'amarilla'),
(2, 1, 108, 23, 'amarilla'),
(3, 1, 105, 35, 'roja'),
(4, 2, 114, 20, 'amarilla'),
(5, 2, 121, 38, 'roja');

