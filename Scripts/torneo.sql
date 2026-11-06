DROP DATABASE IF EXISTS torneo;
CREATE DATABASE torneo;
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
    FOREIGN KEY (id_equipo) REFERENCES equipo(id_equipo) ON DELETE CASCADE,
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
    id_gol INT AUTO_INCREMENT,
    id_partido INT NOT NULL,
    ci_jugador INT NOT NULL,
    minuto INT NOT NULL,
    autogol BOOLEAN NOT NULL,
    PRIMARY KEY (id_gol),
    FOREIGN KEY (id_partido) REFERENCES partido(id_partido),
    FOREIGN KEY (ci_jugador) REFERENCES jugador(ci)
);

CREATE TABLE sancion_jugador (
    id_sancion INT AUTO_INCREMENT,
    ci_jugador INT NOT NULL,
    id_torneo INT NOT NULL,
    motivo ENUM('roja', 'acumulacion de amarillas', 'disciplinaria') NOT NULL,
    numero_fecha_inicio INT NOT NULL,
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

CREATE VIEW torneo.goles_partido AS
SELECT
    id_partido, id_equipo,COUNT(*) AS cantidad_goles
FROM (SELECT
             p.id_partido,
             CASE
                 WHEN g.autogol = TRUE THEN
                     CASE
                         WHEN j.id_equipo = p.id_equipo_local
                             THEN p.id_equipo_visitante
                         ELSE p.id_equipo_local END
                 ELSE j.id_equipo END AS id_equipo
         FROM (SELECT * FROM partido p WHERE p.estado = 'jugado') AS p
                  JOIN torneo.gol g ON p.id_partido = g.id_partido
                  JOIN torneo.planilla_partido j ON j.id_partido = g.id_partido AND j.ci_jugador = g.ci_jugador) AS goles
GROUP BY id_partido, id_equipo;

CREATE VIEW torneo.partidos_jugados AS
SELECT *
        FROM torneo.partido p
        WHERE p.estado='jugado';

DELIMITER $$

CREATE VIEW resultado_partido AS
SELECT
    p.id_partido,
    p.id_equipo_local,
    p.id_equipo_visitante,
    COALESCE(gl.cantidad_goles, 0) AS goles_local,
    COALESCE(gv.cantidad_goles, 0) AS goles_visitante
FROM partidos_jugados p
         LEFT JOIN goles_partido gl
                   ON gl.id_partido = p.id_partido
                       AND gl.id_equipo = p.id_equipo_local
         LEFT JOIN goles_partido gv
                   ON gv.id_partido = p.id_partido
                       AND gv.id_equipo = p.id_equipo_visitante;

CREATE VIEW puntos_partido AS
SELECT
    id_partido, id_equipo_local AS id_equipo,
    CASE
        WHEN goles_local > goles_visitante THEN 3
        WHEN goles_local = goles_visitante THEN 1
        ELSE 0
        END AS puntos
FROM resultado_partido
UNION ALL
SELECT
    id_partido, id_equipo_visitante AS id_equipo,
    CASE
        WHEN goles_visitante > goles_local THEN 3
        WHEN goles_visitante = goles_local THEN 1
        ELSE 0
        END AS puntos
FROM resultado_partido;

# Ver si el nuevo capitan es de la facultad
CREATE TRIGGER verificar_capitan_facultad_bi BEFORE INSERT ON equipo
FOR EACH ROW
BEGIN
    IF(SELECT id_facultad FROM jugador WHERE ci = NEW.ci_capitan) <> NEW.id_facultad THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El capitan debe ser de la facultad del equipo';
    end if;
END$$

CREATE TRIGGER verificar_capitan_facultad_bu BEFORE UPDATE ON equipo
FOR EACH ROW
BEGIN
    IF (SELECT id_facultad FROM jugador WHERE ci = NEW.ci_capitan) <> NEW.id_facultad THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El capitan debe ser de la facultad del equipo';
    end if;
END$$

# Ver si el nuevo capitan esta en el plantel
CREATE TRIGGER verificar_capitan_plantel_bu BEFORE UPDATE ON equipo
FOR EACH ROW
BEGIN
    IF NEW.ci_capitan <> OLD.ci_capitan AND NOT EXISTS(SELECT id_equipo FROM equipo_jugador_torneo WHERE id_equipo = NEW.id_equipo AND ci_jugador = NEW.ci_capitan) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El nuevo capitan debe formar parte del plantel';
    end if;
END$$

# Ver si esta en etapa de inscripcion (ABM)
CREATE TRIGGER verificar_inscripcion_bi BEFORE INSERT ON equipo
FOR EACH ROW
BEGIN
    IF(SELECT estado FROM torneo WHERE id_torneo = NEW.id_torneo) <> 'inscripcion' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Solo se puede crear equipos en fase de inscripcion';
    END if;
END$$

CREATE TRIGGER verificar_inscripcion_bu BEFORE UPDATE ON equipo
FOR EACH ROW
BEGIN
    IF(SELECT estado FROM torneo WHERE id_torneo = OLD.id_torneo) <> 'inscripcion' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Solo se puede modificar equipos en fase de inscripcion';
    end if;
END$$

CREATE TRIGGER verificar_inscripcion_bd BEFORE DELETE ON equipo
FOR EACH ROW
BEGIN
    IF(SELECT estado FROM torneo WHERE id_torneo = OLD.id_torneo) <> 'inscripcion' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Solo se puede eliminar equipos en fase de inscripcion';
    end if;
END$$

# Que el jugador pertenezca a la facultad del equipo
CREATE TRIGGER verificar_jugador_facultad_bi BEFORE INSERT ON equipo_jugador_torneo
FOR EACH ROW
BEGIN
    IF(SELECT id_facultad FROM jugador WHERE ci = NEW.ci_jugador) <> (SELECT id_facultad FROM equipo WHERE id_equipo = NEW.id_equipo) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El jugador debe pertenecer a la facultad del equipo';
    end if;
END$$

# Maximo 2 profesores por plantel
CREATE TRIGGER verificar_maximo_profesores_bi BEFORE INSERT ON equipo_jugador_torneo
FOR EACH ROW
BEGIN
    IF(SELECT tipo FROM jugador WHERE ci = NEW.ci_jugador) IN ('docente', 'funcionario')
        AND (SELECT COUNT(*) FROM equipo_jugador_torneo e JOIN jugador j ON j.ci = e.ci_jugador
                             WHERE e.id_equipo = NEW.id_equipo AND j.tipo IN ('docente', 'funcionario')) >= 2 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT  = 'El plantel admite como maximo 2 docentes o funcionarios';
    end if;
END$$

# Maximo 10 jugadores por plantel
CREATE TRIGGER verificar_maximo_jugadores_bi BEFORE INSERT ON equipo_jugador_torneo
FOR EACH ROW
BEGIN
    IF(SELECT COUNT(*) FROM equipo_jugador_torneo WHERE id_equipo = NEW.id_equipo)>=10 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El plantel tiene el maximo de 10 jugadores';
    end if;
END$$

# Solo se modifica en inscripcion
CREATE TRIGGER verificar_inscripcion_plantel_bi BEFORE INSERT ON equipo_jugador_torneo
FOR EACH ROW
BEGIN
  IF (SELECT estado FROM torneo WHERE id_torneo = NEW.id_torneo) <> 'inscripcion' THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Los planteles solo se modifican durante la inscripción';
  END IF;
END$$

CREATE TRIGGER verificar_inscripcion_plantel_bu BEFORE UPDATE ON equipo_jugador_torneo
FOR EACH ROW
BEGIN
  IF (SELECT estado FROM torneo WHERE id_torneo = OLD.id_torneo) <> 'inscripcion' THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Los planteles solo se modifican durante la inscripción';
  END IF;
END$$

CREATE TRIGGER verificar_inscripcion_plantel_bd BEFORE DELETE ON equipo_jugador_torneo
FOR EACH ROW
BEGIN
  IF (SELECT estado FROM torneo WHERE id_torneo = OLD.id_torneo) <> 'inscripcion' THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Los planteles solo se modifican durante la inscripción';
  END IF;
END$$

# No se puede sacar el capitan del plantel
CREATE TRIGGER evitar_sacar_capitan_bd BEFORE DELETE ON equipo_jugador_torneo
FOR EACH ROW
BEGIN
    IF EXISTS(SELECT id_equipo FROM equipo WHERE id_equipo = OLD.id_equipo AND ci_capitan = OLD.ci_jugador) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No se puede sacar el capitan del equipo';
    end if;
END $$

#No hay enfrentamientos repetidos en un mismo torneo
CREATE TRIGGER validar_enfrentamiento_BI
BEFORE INSERT ON partido
           FOR EACH ROW
BEGIN
    IF EXISTS(
        SELECT *
        FROM partido p
        WHERE p.id_torneo= NEW.id_torneo
        AND p.estado <> 'cancelado'
        AND ((p.id_equipo_local = NEW.id_equipo_local AND p.id_equipo_visitante = NEW.id_equipo_visitante)
        OR (p.id_equipo_visitante = NEW.id_equipo_local AND p.id_equipo_local= NEW.id_equipo_visitante)))
THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Los equipos ya se enfrentaron en este torneo';
    end if;
END $$

CREATE TRIGGER validar_enfrentamiento_BU
    BEFORE UPDATE ON partido
    FOR EACH ROW
BEGIN
    IF EXISTS(
        SELECT *
        FROM partido p
        WHERE p.id_torneo= NEW.id_torneo
          AND p.id_partido <> NEW.id_partido
          AND p.estado <> 'cancelado'
          AND ((p.id_equipo_local = NEW.id_equipo_local AND p.id_equipo_visitante = NEW.id_equipo_visitante)
            OR (p.id_equipo_visitante = NEW.id_equipo_local AND p.id_equipo_local= NEW.id_equipo_visitante)))
    THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Los equipos ya se enfrentaron en este torneo';
    end if;
END $$

#Los dos equipos son del mismo torneo
CREATE TRIGGER validar_equipos_torneo_BI
    BEFORE INSERT ON partido
    FOR EACH ROW
    BEGIN
        if not EXISTS(
            SELECT *
            FROM equipo e
            where e.id_torneo=NEW.id_torneo AND
                NEW.id_equipo_local = e.id_equipo
        ) then
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'El equipo local no está en el torneo';
        end if;
        if not EXISTS(
                SELECT *
                FROM equipo e
                WHERE e.id_torneo=NEW.id_torneo AND
                         NEW.id_equipo_visitante= e.id_equipo
            ) then
                SIGNAL SQLSTATE '45000'
                    SET MESSAGE_TEXT = 'El equipo visitante no está en el torneo';
            end if;
        end $$

CREATE TRIGGER validar_equipos_torneo_BU
    BEFORE UPDATE ON partido
    FOR EACH ROW
BEGIN
    if not EXISTS(
        SELECT *
        FROM equipo e
        where e.id_torneo=NEW.id_torneo AND
            NEW.id_equipo_local = e.id_equipo
    ) then
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'El equipo local no está en el torneo';
    end if;
    if not EXISTS(
        SELECT *
        FROM equipo e
        WHERE e.id_torneo=NEW.id_torneo AND
            NEW.id_equipo_visitante= e.id_equipo
    ) then
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'El equipo visitante no está en el torneo';
    end if;
end $$

#Los equipos tiene más de 5 jugadores
CREATE TRIGGER validar_cantidad_jugadores_BI
    BEFORE INSERT ON partido
    FOR EACH ROW
BEGIN
    IF (SELECT COUNT(*)
        FROM equipo_jugador_torneo ej
        WHERE ej.id_equipo = NEW.id_equipo_local
        AND ej.id_torneo = NEW.id_torneo
       ) < 5 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'El equipo local debe tener al menos 5 jugadores';
    END IF;
    IF (SELECT COUNT(*)
        FROM equipo_jugador_torneo ej
        WHERE ej.id_equipo = NEW.id_equipo_visitante
        AND ej.id_torneo = NEW.id_torneo
       ) < 5 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'El equipo visitante debe tener al menos 5 jugadores';
    END IF;
    END $$

#Un mismo equipo no se enfrenta consigo mismo
CREATE TRIGGER validar_equipo_BI
    BEFORE INSERT ON partido
    FOR EACH ROW
BEGIN
    IF NEW.id_equipo_local= NEW.id_equipo_visitante
    Then
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Un mismo equipo no puede enfrentarse a si mismo';
    end if;
END $$

CREATE TRIGGER validar_equipo_BU
    BEFORE UPDATE ON partido
    FOR EACH ROW
BEGIN
    IF NEW.id_equipo_local= NEW.id_equipo_visitante
    Then
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Un mismo equipo no puede enfrentarse a si mismo';
    end if;
END $$

#Un equipo no juegue dos partidos en la misma fecha
CREATE TRIGGER validar_equipodisponible_BI
    BEFORE INSERT ON partido
    FOR EACH ROW
BEGIN
    IF EXISTS(
        SELECT *
        FROM partido p
        WHERE p.id_torneo = NEW.id_torneo
          AND p.numero_fecha= NEW.numero_fecha
          AND p.estado <> 'cancelado'
          AND (p.id_equipo_local = NEW.id_equipo_local OR p.id_equipo_visitante = NEW.id_equipo_visitante
            OR p.id_equipo_visitante = NEW.id_equipo_local OR p.id_equipo_local= NEW.id_equipo_visitante))
    THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Alguno de los equipos ya juega un partido en esa fecha';
    end if;
END $$

CREATE TRIGGER validar_equipodisponible_BU
    BEFORE UPDATE ON partido
    FOR EACH ROW
BEGIN
    IF EXISTS(
        SELECT *
        FROM partido p
        WHERE p.id_torneo = NEW.id_torneo
          AND p.id_partido <> NEW.id_partido
          AND p.numero_fecha= NEW.numero_fecha
          AND p.estado <> 'cancelado'
          AND (p.id_equipo_local = NEW.id_equipo_local OR p.id_equipo_visitante = NEW.id_equipo_visitante
            OR p.id_equipo_visitante = NEW.id_equipo_local OR p.id_equipo_local= NEW.id_equipo_visitante))
    THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Alguno de los equipos ya juega un partido en esa fecha';
    end if;
END $$

#No hay dos partidos en la misma cancha, día y turno
CREATE TRIGGER validar_canchadisponible_BI
    BEFORE INSERT ON partido
    FOR EACH ROW
BEGIN
    IF EXISTS(
        SELECT *
        FROM partido p
        WHERE p.estado <>'cancelado'
          AND p.dia = NEW.dia
          AND p.nombre_cancha = NEW.nombre_cancha
          AND p.id_complejo = NEW.id_complejo
          AND p.id_turno = NEW.id_turno)
    THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Ya hay un partido en esa cancha, ese día y en ese turno';
    end if;
END $$

CREATE TRIGGER validar_canchadisponible_BU
    BEFORE UPDATE ON partido
    FOR EACH ROW
BEGIN
    IF EXISTS(
        SELECT *
        FROM partido p
        WHERE p.id_partido <> NEW.id_partido
          AND p.estado <>'cancelado'
          AND p.dia = NEW.dia
          AND p.nombre_cancha = NEW.nombre_cancha
          AND p.id_complejo = NEW.id_complejo
          AND p.id_turno = NEW.id_turno)
    THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Ya hay un partido en esa cancha, ese día y en ese turno';
    end if;
END $$

#Un partido jugado no puede eliminarse
CREATE TRIGGER no_eliminacion_partido_BD
    BEFORE DELETE on partido
    FOR EACH ROW
    BEGIN
        if old.estado= 'jugado'
        THEN
            SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'No se puede borrar un partido que ya se jugó';
        end if;
    end $$

#Actualizacion de un partido a jugado si no pasó la fecha
CREATE TRIGGER modificacion_a_jugado_BU
    BEFORE  UPDATE on partido
    FOR EACH ROW
    BEGIN
        if new.estado= 'jugado'AND OLD.estado <> 'jugado'
            then
            if CURDATE()<OLD.dia
                then
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'No se puede actualizar a jugado si no pasó la fecha del partido';
                end if;
        end if;
    end $$

CREATE TRIGGER validar_jugador_planilla
    BEFORE INSERT ON planilla_partido
    FOR EACH ROW
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM partido p
                 INNER JOIN equipo_jugador_torneo ej
                            ON ej.id_torneo = p.id_torneo
        WHERE p.id_partido = NEW.id_partido
          AND ej.ci_jugador = NEW.ci_jugador
          AND ej.id_equipo = NEW.id_equipo
          AND (
            p.id_equipo_local = NEW.id_equipo
                OR p.id_equipo_visitante = NEW.id_equipo
            )
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT =
                    'El jugador no pertenece al plantel del equipo indicado o el equipo no participa en el partido';
    END IF;
END $$

CREATE TRIGGER validar_suspension_planilla
    BEFORE INSERT ON planilla_partido
    FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT 1
        FROM partido p
                 INNER JOIN sancion_jugador s
                            ON s.ci_jugador = NEW.ci_jugador
                                AND s.id_torneo = p.id_torneo
        WHERE p.id_partido = NEW.id_partido
          AND p.numero_fecha >= s.numero_fecha_inicio
          AND p.numero_fecha <
              s.numero_fecha_inicio + s.cantidad_fechas
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT =
                    'El jugador esta suspendido y no puede integrar la planilla';

    END IF;
END $$

CREATE TRIGGER controlar_update_planilla
    BEFORE UPDATE ON planilla_partido
    FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT 1
        FROM partido
        WHERE id_partido = OLD.id_partido
          AND estado = 'jugado'
          AND DATEDIFF(CURDATE(), dia) > 2
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Se superaron las 48 horas del partido';
    END IF;
END $$

CREATE TRIGGER controlar_delete_planilla
    BEFORE DELETE ON planilla_partido
    FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT 1
        FROM partido
        WHERE id_partido = OLD.id_partido
          AND estado = 'jugado'
          AND DATEDIFF(CURDATE(), dia) > 2
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Se superaron las 48 horas del partido';
    END IF;
END $$

CREATE TRIGGER controlar_insert_planilla
    BEFORE INSERT ON planilla_partido
    FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT 1
        FROM partido
        WHERE id_partido = NEW.id_partido
          AND estado = 'jugado'
          AND DATEDIFF(CURDATE(), dia) > 2
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Se superaron las 48 horas del partido';
    END IF;
END $$

CREATE TRIGGER controlar_insert_gol
    BEFORE INSERT ON gol
    FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT 1
        FROM partido
        WHERE id_partido = NEW.id_partido
          AND estado = 'jugado'
          AND DATEDIFF(CURDATE(), dia) > 2
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Se superaron las 48 horas del partido';
    END IF;
END $$

CREATE TRIGGER controlar_update_gol
    BEFORE UPDATE ON gol
    FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT 1
        FROM partido
        WHERE id_partido = OLD.id_partido
          AND estado = 'jugado'
          AND DATEDIFF(CURDATE(), dia) > 2
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Se superaron las 48 horas del partido';
    END IF;
END $$

CREATE TRIGGER controlar_delete_gol
    BEFORE DELETE ON gol
    FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT 1
        FROM partido
        WHERE id_partido = OLD.id_partido
          AND estado = 'jugado'
          AND DATEDIFF(CURDATE(), dia) > 2
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Se superaron las 48 horas del partido';
    END IF;
END $$

CREATE TRIGGER controlar_insert_tarjeta
    BEFORE INSERT ON tarjeta
    FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT 1
        FROM partido
        WHERE id_partido = NEW.id_partido
          AND estado = 'jugado'
          AND DATEDIFF(CURDATE(), dia) > 2
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Se superaron las 48 horas del partido';
    END IF;
END $$

CREATE TRIGGER controlar_update_tarjeta
    BEFORE UPDATE ON tarjeta
    FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT 1
        FROM partido
        WHERE id_partido = OLD.id_partido
          AND estado = 'jugado'
          AND DATEDIFF(CURDATE(), dia) > 2
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Se superaron las 48 horas del partido';
    END IF;
END $$

CREATE TRIGGER controlar_delete_tarjeta
    BEFORE DELETE ON tarjeta
    FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT 1
        FROM partido
        WHERE id_partido = OLD.id_partido
          AND estado = 'jugado'
          AND DATEDIFF(CURDATE(), dia) > 2
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Se superaron las 48 horas del partido';
    END IF;
END $$

CREATE TRIGGER sancion_por_roja
    AFTER INSERT ON tarjeta
    FOR EACH ROW
BEGIN
    IF NEW.color = 'roja' THEN
        INSERT INTO sancion_jugador (ci_jugador, id_torneo, motivo, numero_fecha_inicio, cantidad_fechas)
        SELECT NEW.ci_jugador, p.id_torneo, 'roja', p.numero_fecha + 1, 1
          FROM partido p
         WHERE p.id_partido = NEW.id_partido;
    END IF;
END $$

CREATE TRIGGER sancion_por_amarillas
    AFTER INSERT ON tarjeta
    FOR EACH ROW
BEGIN
    IF NEW.color = 'amarilla' THEN
        INSERT INTO sancion_jugador (ci_jugador, id_torneo, motivo, numero_fecha_inicio, cantidad_fechas)
        SELECT NEW.ci_jugador, p.id_torneo, 'acumulacion de amarillas', p.numero_fecha + 1, 1
          FROM partido p
         WHERE p.id_partido = NEW.id_partido
           AND (SELECT COUNT(*)
                  FROM tarjeta t
                  JOIN partido p2 ON p2.id_partido = t.id_partido
                 WHERE t.ci_jugador = NEW.ci_jugador
                   AND t.color = 'amarilla'
                   AND p2.id_torneo = p.id_torneo) % 3 = 0;
    END IF;
END $$

CREATE TRIGGER validar_sancion
    BEFORE INSERT ON sancion_jugador
    FOR EACH ROW
BEGIN
    IF NEW.cantidad_fechas < 1 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT =
                    'La sancion debe tener al menos una fecha';
    END IF;
    IF NOT EXISTS (
        SELECT 1
        FROM equipo_jugador_torneo
        WHERE ci_jugador = NEW.ci_jugador
          AND id_torneo = NEW.id_torneo
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT =
                    'El jugador no esta inscripto en este torneo';
    END IF;
END $$

DELIMITER ;

INSERT INTO facultad (id_facultad, nombre) VALUES
(1, 'Facultad de Ingenieria'),
(2, 'Facultad de Ciencias Empresariales'),
(3, 'Facultad de Derecho'),
(4, 'Facultad de Psicologia');

INSERT INTO torneo (id_torneo, nombre, anio, semestre, fecha_inicio, fecha_fin, estado) VALUES
(1, 'Copa Universitaria', 2026, '2', '2026-11-01', '2026-11-30', 'inscripcion');

INSERT INTO login (correo, contrasena, rol) VALUES
('admin@ucu.edu.uy', '$2b$12$CbPV7.b/01UKBSWLq54FL.rD8oFUmASfB/JSLUBXQP85I0qqwnmOe', 'administrador'),
('planillero1@ucu.edu.uy', '$2b$12$Ri7W4eKb.BZEt92PQDN39e8CUW35fkID1T4WAZCR7BdDdPw8g4MyS', 'planillero'),
('planillero2@ucu.edu.uy', '$2b$12$2sHBDtXH2l/kJwVonHJ7cu2wV.grytgMdMROjlk.fleKhi2PLjq3O', 'planillero');

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
(110, 'Agustin', 'Torres', 'agus@gmail.com', '2001-12-05', 2, 'posgrado'),
(111, 'Bruno', 'Diaz', 'bruno@gmail.com', '2002-02-14', 2, 'grado'),
(112, 'Tomas', 'Romero', 'tomas@gmail.com', '2000-10-30', 2, 'docente'),
(113, 'Andres', 'Alonso', 'andres@gmail.com', '2001-03-19', 1, 'grado'),
(114, 'Facundo', 'Castro', 'facu@gmail.com', '2002-06-21', 1, 'grado'),
(115, 'Gabriel', 'Mendez', 'gabriel@gmail.com', '2000-12-11', 1, 'grado'),
(116, 'Ignacio', 'Vazquez', 'ignacio@gmail.com', '2001-08-08', 1, 'grado'),
(117, 'Joaquin', 'Ramos', 'joaquin@gmail.com', '2002-01-17', 1, 'grado'),
(118, 'Franco', 'Pereira', 'franco@gmail.com', '2000-05-09', 1, 'funcionario'),
(119, 'Emiliano', 'Acosta', 'emi@gmail.com', '2001-02-25', 2, 'grado'),
(120, 'Matias', 'Benitez', 'matias@gmail.com', '2002-04-13', 2, 'grado'),
(121, 'Sebastian', 'Cabrera', 'seba@gmail.com', '2000-07-07', 2, 'grado'),
(122, 'Maximiliano', 'Duarte', 'maxi@gmail.com', '2001-10-16', 2, 'grado'),
(123, 'Valentin', 'Etcheverry', 'valen@gmail.com', '2002-09-03', 2, 'grado'),
(124, 'Benjamin', 'Farias', 'benja@gmail.com', '2000-11-28', 2, 'posgrado'),
(125, 'Carlos', 'Vera', 'carlos@gmail.com', '2001-06-02', 3, 'grado'),
(126, 'Hugo', 'Pinto', 'hugo@gmail.com', '2002-03-27', 3, 'grado'),
(127, 'Ramiro', 'Sosa', 'ramiro@gmail.com', '2000-09-14', 3, 'grado'),
(128, 'Lucio', 'Paz', 'lucio@gmail.com', '2001-11-30', 3, 'grado'),
(129, 'Bautista', 'Rey', 'bautista@gmail.com', '2002-08-19', 3, 'grado'),
(130, 'Ciro', 'Luna', 'ciro@gmail.com', '1985-04-05', 3, 'docente'),
(131, 'Renzo', 'Mora', 'renzo@gmail.com', '2001-01-23', 4, 'grado'),
(132, 'Thiago', 'Nunez', 'thiago@gmail.com', '2002-05-11', 4, 'grado'),
(133, 'Leandro', 'Ibarra', 'leandro@gmail.com', '2000-12-29', 4, 'grado'),
(134, 'Damian', 'Rios', 'damian@gmail.com', '2001-07-16', 4, 'grado'),
(135, 'Enzo', 'Salas', 'enzo@gmail.com', '2002-10-08', 4, 'grado'),
(136, 'Mauro', 'Vega', 'mauro@gmail.com', '1980-02-18', 4, 'funcionario');

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
(4, 'Los Contadores', 1, 2, 119),
(5, 'Los Abogados', 1, 3, 125),
(6, 'Los Psicologos', 1, 4, 131);

INSERT INTO equipo_jugador_torneo (id_equipo, ci_jugador, id_torneo, numero_camiseta) VALUES
(1, 101, 1, 1), (1, 102, 1, 2), (1, 103, 1, 3), (1, 104, 1, 4), (1, 105, 1, 5), (1, 106, 1, 6),
(2, 107, 1, 1), (2, 108, 1, 2), (2, 109, 1, 3), (2, 110, 1, 4), (2, 111, 1, 5), (2, 112, 1, 6),
(3, 113, 1, 1), (3, 114, 1, 2), (3, 115, 1, 3), (3, 116, 1, 4), (3, 117, 1, 5), (3, 118, 1, 6),
(4, 119, 1, 1), (4, 120, 1, 2), (4, 121, 1, 3), (4, 122, 1, 4), (4, 123, 1, 5), (4, 124, 1, 6),
(5, 125, 1, 1), (5, 126, 1, 2), (5, 127, 1, 3), (5, 128, 1, 4), (5, 129, 1, 5), (5, 130, 1, 6),
(6, 131, 1, 1), (6, 132, 1, 2), (6, 133, 1, 3), (6, 134, 1, 4), (6, 135, 1, 5), (6, 136, 1, 6);

INSERT INTO partido (id_partido, id_torneo, numero_fecha, id_equipo_local, id_equipo_visitante, dia, id_turno, nombre_cancha, id_complejo, estado) VALUES
(1, 1, 1, 1, 6, '2026-11-01', 1, 'Cancha 1', 1, 'programado'),
(2, 1, 1, 2, 5, '2026-11-01', 1, 'Cancha 2', 1, 'programado'),
(3, 1, 1, 3, 4, '2026-11-01', 2, 'Cancha 1', 2, 'programado'),
(4, 1, 2, 1, 5, '2026-11-03', 1, 'Cancha 1', 1, 'programado'),
(5, 1, 2, 6, 4, '2026-11-03', 2, 'Cancha 2', 2, 'programado'),
(6, 1, 2, 2, 3, '2026-11-03', 3, 'Cancha 1', 1, 'programado'),
(7, 1, 3, 1, 4, '2026-11-04', 1, 'Cancha 1', 1, 'programado'),
(8, 1, 3, 5, 3, '2026-11-04', 2, 'Cancha 2', 1, 'programado'),
(9, 1, 3, 6, 2, '2026-11-04', 3, 'Cancha 1', 2, 'programado'),
(10, 1, 4, 1, 3, '2026-11-10', 1, 'Cancha 1', 1, 'programado'),
(11, 1, 4, 4, 2, '2026-11-10', 2, 'Cancha 2', 1, 'programado'),
(12, 1, 4, 5, 6, '2026-11-10', 3, 'Cancha 1', 2, 'programado'),
(13, 1, 5, 1, 2, '2026-11-12', 1, 'Cancha 1', 1, 'postergado'),
(14, 1, 5, 3, 6, '2026-11-12', 2, 'Cancha 2', 1, 'cancelado'),
(15, 1, 5, 4, 5, '2026-11-12', 3, 'Cancha 1', 2, 'programado');

INSERT INTO planilla_partido (id_partido, ci_jugador, id_equipo)
SELECT p.id_partido, ej.ci_jugador, ej.id_equipo
FROM partido p
JOIN equipo_jugador_torneo ej
  ON ej.id_equipo IN (p.id_equipo_local, p.id_equipo_visitante)
WHERE p.id_partido <= 9
  AND ej.numero_camiseta <= 5;

INSERT INTO sancion_jugador (ci_jugador, id_torneo, motivo, numero_fecha_inicio, cantidad_fechas) VALUES
(106, 1, 'disciplinaria', 2, 2);

INSERT INTO gol (id_gol, id_partido, ci_jugador, minuto, autogol) VALUES
(1, 1, 101, 10, FALSE),
(2, 1, 102, 25, FALSE),
(3, 1, 131, 15, FALSE),
(4, 2, 107, 12, FALSE),
(5, 2, 125, 30, FALSE),
(6, 2, 126, 38, FALSE),
(7, 3, 113, 8, FALSE),
(8, 3, 119, 20, FALSE),
(9, 3, 120, 40, TRUE),
(10, 4, 101, 5, FALSE),
(11, 4, 125, 18, FALSE),
(12, 4, 127, 33, FALSE),
(13, 4, 103, 40, FALSE),
(14, 5, 132, 14, FALSE),
(15, 5, 133, 26, FALSE),
(16, 5, 121, 31, FALSE),
(17, 6, 107, 9, FALSE),
(18, 6, 113, 22, FALSE),
(19, 6, 114, 37, FALSE),
(20, 7, 101, 11, FALSE),
(21, 7, 104, 24, FALSE),
(22, 7, 103, 34, FALSE),
(23, 7, 119, 36, FALSE),
(24, 8, 125, 7, FALSE),
(25, 8, 115, 29, FALSE),
(26, 9, 110, 16, FALSE),
(27, 9, 108, 21, FALSE),
(28, 9, 134, 35, FALSE);

INSERT INTO tarjeta (id_tarjeta, id_partido, ci_jugador, minuto, color) VALUES
(1, 1, 102, 18, 'amarilla'),
(2, 1, 131, 23, 'amarilla'),
(3, 2, 108, 20, 'amarilla'),
(4, 3, 114, 33, 'amarilla'),
(5, 4, 102, 30, 'amarilla'),
(6, 4, 126, 36, 'amarilla'),
(7, 5, 120, 12, 'amarilla'),
(8, 6, 109, 27, 'amarilla'),
(9, 7, 102, 26, 'amarilla'),
(10, 7, 122, 38, 'roja'),
(11, 8, 127, 19, 'amarilla'),
(12, 9, 111, 35, 'roja');

UPDATE partido SET estado = 'jugado' WHERE id_partido BETWEEN 1 AND 9;
UPDATE torneo SET estado = 'en curso' WHERE id_torneo = 1;


CREATE USER IF NOT EXISTS 'admin_app'@'%' IDENTIFIED BY 'admin_pass';
CREATE USER IF NOT EXISTS 'planillero_app'@'%' IDENTIFIED BY 'planillero_pass';
CREATE USER IF NOT EXISTS 'lector_app'@'%' IDENTIFIED BY 'lector_pass';
GRANT SELECT ON torneo.* TO 'lector_app'@'%';
GRANT ALL PRIVILEGES ON torneo.* TO 'admin_app'@'%';

GRANT SELECT ON torneo.* TO 'planillero_app'@'%';
GRANT INSERT, UPDATE, DELETE ON torneo.planilla_partido TO 'planillero_app'@'%';
GRANT INSERT, UPDATE, DELETE ON torneo.gol TO 'planillero_app'@'%';
GRANT INSERT, UPDATE, DELETE ON torneo.tarjeta TO 'planillero_app'@'%';
FLUSH PRIVILEGES;