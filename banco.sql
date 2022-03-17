CREATE TABLE Usuario 
( 
 UsuarioId INT PRIMARY KEY AUTO_INCREMENT,  
 usuarioNome VARCHAR(n) NOT NULL,  
 UsuarioPassword VARCHAR(n) NOT NULL,  
); 

CREATE TABLE arquivos 
( 
 fk_idUsuario INT,  
 id INT PRIMARY KEY,  
 uuid VARCHAR(n) NOT NULL,  
 Private INT NOT NULL DEFAULT '1',  
); 

ALTER TABLE arquivos ADD FOREIGN KEY(fk_idUsuario) REFERENCES Usuario (fk_idUsuario)

