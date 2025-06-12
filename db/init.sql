-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS hc_bfa;
USE hc_bfa;

-- Eliminar tablas si existen (para desarrollo)
DROP TABLE IF EXISTS historias;
DROP TABLE IF EXISTS pacientes;
DROP TABLE IF EXISTS usuarios;

-- Tabla de pacientes
CREATE TABLE pacientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dni VARCHAR(20) NOT NULL UNIQUE,
    apellido VARCHAR(100) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE,
    sexo ENUM('Masculino', 'Femenino', 'Otro') DEFAULT NULL
);

-- Tabla de usuarios
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    rol ENUM('Admin', 'Doctor', 'Enfermero', 'Tecnico') NOT NULL
);

-- Tabla de historias clínicas
CREATE TABLE historias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT NOT NULL,
    usuario_id INT NOT NULL,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    motivo_consulta TEXT,
    antecedentes TEXT,
    examen_fisico TEXT,
    diagnostico TEXT,
    tratamiento TEXT,
    observaciones TEXT,
    hash CHAR(64) NOT NULL,
    tx_hash VARCHAR(100),
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- Índices útiles para búsqueda
CREATE INDEX idx_pacientes_dni ON pacientes (dni);
CREATE INDEX idx_pacientes_nombre ON pacientes (nombre);
CREATE INDEX idx_pacientes_apellido ON pacientes (apellido);

-- Usuario administrador inicial (solo si no existe)
INSERT INTO usuarios (nombre, username, email, password_hash, rol)
SELECT 'Admin', 'admin', 'admin@ejemplo.com',
'scrypt:32768:8:1$A63POXMoCCciR0XF$f0aa4fe424e8bbd4653bfb8cd9a3d511b705c147f1ab669765cb62800253d866a756ce4d2d060fac95b127a02a1dc79316cd50ec7ebc37a60bd4901b6d039252',
'Admin'
WHERE NOT EXISTS (
    SELECT 1 FROM usuarios WHERE username = 'admin'
);
