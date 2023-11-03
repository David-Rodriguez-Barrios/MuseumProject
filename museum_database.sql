DROP DATABASE IF EXISTS museum_database;
CREATE DATABASE museum_database; 
USE museum_database;

DROP TABLE IF EXISTS ARTIST;
CREATE TABLE ARTIST (
	Name			VARCHAR(50)		NOT NULL,
    Description		VARCHAR(300),
    Main_style		VARCHAR(50),
    Date_died		INT,
    Date_born		INT,
    Epoch			VARCHAR(50),
    COO				VARCHAR(50),
    
	primary key (Name)
);
INSERT INTO ARTIST (Name, Description, Main_style, Date_died, Date_born, Epoch, COO)
VALUES
('Hans Eworth', 'Exiled Flemings', 'Allegorical images and portraits', 1574, 1520, 'Early Modern Period', 'England'),
('Jacques I Androuet du Cerceau', 'French designer', 'Renaissance architecture', 1585, 1510, 'Early Modern Period', 'France'),
('Nicholas Hilliard','whole face in the presence of the sitter', NULL, 1619, 1547, 'The Elizabethan era','London, England'),
('George Gower', 'Seldom is known but he was a grandson of Sir Gower of Stittenham', 'Oil Paintings', 1540, 1596, 'Tudor period', 'England'),
('Affabel Partridge', 'Partridge was a London goldsmith who served Elizabeth I.', 'Jewellery', NULL, NULL, 'Tudor period', 'England'),
('Pier Jacopo','Italian Sculptor in the renaissance known for the refined interpretation of the Antique.','Italian-Mantua renaissance',1528,1460,'Middle Ages','Italy'),
('Marpuah','Javanese Hindi Religious Sculptor','Hindi Sculptor',700,740,'Pre Angkor','Indonesia');


DROP TABLE IF EXISTS ART_OBJECT;    
CREATE TABLE ART_OBJECT (
	Id_no			INT			    NOT NULL,
    Title			VARCHAR(50),
    Year			INT,
    Description		VARCHAR(300),
    Epoch			VARCHAR(50),
    COO				VARCHAR(50),
    Artist			VARCHAR(50),
    
	primary key (id_no),
    foreign key (Artist) references ARTIST(Name)
        ON DELETE CASCADE      ON UPDATE CASCADE
);

INSERT INTO ART_OBJECT (Id_no, Title, Year, Description, Epoch, COO, Artist)
VALUES
(001, 'Mary I', 1554, 'Queen of England', 'Early Modern Period', 'England', 'Hans Eworth'),
(003,'Paris',1518,'Paris holds the golden apple to be awarded to the goddess.','Middle Ages','Italy','Pier Jacopo Alari Bonacolsi'),
(004, 'Elizabeth I (The Hampden Portrait)', 1567, 'Queen of England, Tudor period', NULL,'England', 'George Gower'),
(006, 'Tankard', 1575, 'A golden cup', 'England', NULL, 'Affabel Partridge'),
(007,'The Heneage Jewel', 1595, 'Enameled gold, table-cut diamonds, and  Burmese rubies.', 'The Elizabethan era', 'London, England', 'Nicholas Hilliard'),
(999, 'The "Sea-Dog" Table', 1575, 'Four mythical chimaera', 'Early Modern Period', 'France', 'Jacques I Androuet du Cerceau'),
(009,'Standing Four-Armed Shiva',700,'Statue one of the principal deities of Hinduism, Shiva','Pre-Angkor','Indonesia','Marpuah');


DROP TABLE IF EXISTS COLLECTIONS;
CREATE TABLE COLLECTIONS (
	Name			VARCHAR(15)		NOT NULL,
    Address			VARCHAR(50),
    Type			VARCHAR(15),
    Contact_person	VARCHAR(30),
    Description		VARCHAR(300),
    Phone			VARCHAR(15),
    
	primary key (Name)
);
INSERT INTO COLLECTIONS (Name, Address, Type, Contact_person, Description, Phone)
VALUES
('Collection 1', '4678 Sharon Lane', 'Museum', 'John', 'Employee favourites', '234 567 1111'),
('Browns', '479 Sherbert Drive', 'Personal', 'Jimmy Smith','Family Heirlooms that get rented out', '533 965 9871');

DROP TABLE IF EXISTS OTHER;
CREATE TABLE OTHER (
	Id_no			INT		NOT NULL,
    Style			VARCHAR(50),
    Type			VARCHAR(50),
    
	primary key (Id_no),
    foreign key (Id_no) references ART_OBJECT(Id_no)
        ON DELETE CASCADE      ON UPDATE CASCADE
);

INSERT INTO OTHER (Id_no, Style, Type)
VALUES
(999, 'Furniture', 'Table'),
(007,'Jewellery','Locket'),
(006,'Fluid Holding Device', 'Cup');

DROP TABLE IF EXISTS PAINTING;
CREATE TABLE PAINTING (
	Id_no			INT		NOT NULL,
    Drawn_on		VARCHAR(50),
    Paint_type		VARCHAR(50),
    Style			VARCHAR(50),
    
	primary key (Id_no),
    foreign key (Id_no) references ART_OBJECT(Id_no)
        ON DELETE CASCADE      ON UPDATE CASCADE
);
INSERT INTO PAINTING (Id_no, Drawn_on, Paint_type,Style)
VALUES
(001, 'Panel', 'Oil', 'Portrait'),
(004, 'Canvas', 'Oil', NULL);


DROP TABLE IF EXISTS SCULPTURE_STATUE;
CREATE TABLE SCULPTURE_STATUE (
	Id_no			INT		NOT NULL,
    Weight		    FLOAT,
    Material		VARCHAR(50),
    Style			VARCHAR(50),
    Height          FLOAT,
    
	primary key (Id_no),
    foreign key (Id_no) references ART_OBJECT(Id_no)
        ON DELETE CASCADE      ON UPDATE CASCADE
);
INSERT INTO SCULPTURE_STATUE (Id_no, Weight, Material,Style,Height)
VALUES
(003, NULL, 'Bronze silver in lay', 'Italian-Mantua', 37.1),
(009,NULL,'Gilt bronze','Pre-Angkor Religious Statue',27.9);

DROP TABLE IF EXISTS BORROWED;
CREATE TABLE BORROWED (
	Id_no			INT		NOT NULL,
	Date_borrowed	DATE,
    Date_returned	DATE,
    Collection_N	VARCHAR(15),
    
	primary key (Id_no),
    foreign key (Id_no) references ART_OBJECT(Id_no)
        ON DELETE CASCADE      ON UPDATE CASCADE,
    foreign key (Collection_N) references COLLECTIONS(Name)
        ON DELETE CASCADE      ON UPDATE CASCADE
);
INSERT INTO BORROWED (Id_no, Date_borrowed, Date_returned,Collection_N)
VALUES
(001, '2001-01-01', '2099-01-01', 'Collection 1'),
(007, '2012-10-10', '2023-01-08', 'Browns');

DROP TABLE IF EXISTS PERMANENT_C;
CREATE TABLE PERMANENT_C (
	Id_no			INT	        NOT NULL,
    Date_acquired	DATE,
    Cost			FLOAT,
    Status			VARCHAR(15),
    
	primary key (Id_no),
    foreign key (Id_no) references ART_OBJECT(Id_no)
        ON DELETE CASCADE      ON UPDATE CASCADE
);
INSERT INTO PERMANENT_C (Id_no, Date_acquired, Cost, Status)
VALUES
(999, '2015-03-12', 1500000, 'stored'),
(004, '1910-04-15', 10000, 'loaned'),
(006, '1924-07-15', 48000, 'loaned'),
(003, '1955-06-28', NULL, 'on display'),
(009, '1994-11-09', NULL,'on display');

DROP TABLE IF EXISTS EXHIBITIONS;
CREATE TABLE EXHIBITIONS (
	Name			VARCHAR(50)		NOT NULL,
    Start_date	    DATE,
    End_date		DATE,
    
	primary key (Name)
);
INSERT INTO EXHIBITIONS (Name, Start_date, End_date)
VALUES
('Exhibition 1', '2012-01-09', '2020-04-14'),
('The Tudors: Art and Majesty in Renaissance England', '2022-10-10', '2023-01-08'),
('Asian Art: At The MET','2004-05-06',NULL),
('The Frick Collection', '1998-09-21', NULL);

DROP TABLE IF EXISTS DISPLAYED_IN;
CREATE TABLE DISPLAYED_IN (
	Id_no			INT		NOT NULL,
    Name			VARCHAR(50),
    
	primary key (Id_no,Name),
    foreign key (Id_no) references ART_OBJECT(Id_no)
        ON DELETE CASCADE      ON UPDATE CASCADE,
    foreign key (Name) references EXHIBITIONS(Name)
        ON DELETE CASCADE      ON UPDATE CASCADE
);
INSERT INTO DISPLAYED_IN (Id_no, Name)
VALUES
(999, 'Exhibition 1'),
(001, 'Exhibition 1'),
(003, 'The Frick Collection'),
(004, 'The Tudors: Art and Majesty in Renaissance England'),
(007, 'The Tudors: Art and Majesty in Renaissance England'),
(006, 'The Tudors: Art and Majesty in Renaissance England'),
(009,'Asian Art: At The MET');

DROP ROLE IF EXISTS db_Admin@localhost, dataEntry@localhost, Guest@localhost;
CREATE ROLE db_Admin@localhost, dataEntry@localhost, Guest@localhost;

GRANT ALL PRIVILEGES ON *.* TO db_Admin@localhost;
GRANT INSERT ON museum_database.* TO dataEntry@localhost;
GRANT UPDATE ON museum_database.* TO dataEntry@localhost;
GRANT DELETE ON museum_database.* TO dataEntry@localhost;
GRANT SELECT ON museum_database.* TO dataEntry@localhost;
GRANT SELECT ON museum_database.* TO Guest@localhost;

DROP USER IF EXISTS mk@localhost, dataMaker@localhost, guest@localhost;

CREATE USER mk@localhost IDENTIFIED BY 'password';
CREATE USER dataMaker@localhost IDENTIFIED BY 'userpass';
CREATE USER guest@localhost;

GRANT db_Admin@localhost TO mk@localhost;
GRANT dataEntry@localhost TO dataMaker@localhost;
GRANT Guest@localhost TO guest@localhost;

SET DEFAULT ROLE ALL TO mk@localhost;
SET DEFAULT ROLE ALL TO dataMaker@localhost;
SET DEFAULT ROLE ALL TO guest@localhost;

FLUSH PRIVILEGES;
