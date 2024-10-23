CREATE DATABASE if not  EXISTS `db_banco`;
USE `db_banco`;


CREATE TABLE IF NOT EXISTS usuarios (
   id INT AUTO_INCREMENT PRIMARY KEY,
   email TEXT NOT NULL,
   senha TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tarefas (
   id INT AUTO_INCREMENT PRIMARY KEY,
   usuario_id INT NOT NULL,
   titulo TEXT NOT NULL,
   conteudo TEXT NOT NULL,
   data DATE,
   limit_data DATE,
   status TEXT NOT NULL,
   prioridade TEXT NOT NULL,
   categoria TEXT NOT NULL,
   FOREIGN KEY (usuario_id) references usuarios(id)

);

