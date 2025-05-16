-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS hc_bfa;
USE hc_bfa;

-- Tabla de pacientes
CREATE TABLE IF NOT EXISTS pacientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    dni VARCHAR(20) NOT NULL UNIQUE
);

-- Tabla de historias clínicas
CREATE TABLE IF NOT EXISTS historias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT NOT NULL,
    fecha DATETIME NOT NULL,
    contenido TEXT NOT NULL,
    hash CHAR(64) NOT NULL,
    tx_hash VARCHAR(100),  -- Nuevo campo para guardar el hash de la transacción en la BFA
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
);

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
);

-- Crear usuario 'hector' solo si no existe ya
INSERT INTO usuarios (nombre, username, password_hash)
SELECT 'Admin', 'admin', 'scrypt:32768:8:1$A63POXMoCCciR0XF$f0aa4fe424e8bbd4653bfb8cd9a3d511b705c147f1ab669765cb62800253d866a756ce4d2d060fac95b127a02a1dc79316cd50ec7ebc37a60bd4901b6d039252'
WHERE NOT EXISTS (
    SELECT 1 FROM usuarios WHERE username = 'admin'
);
