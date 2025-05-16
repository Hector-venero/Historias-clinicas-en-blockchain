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
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
);

