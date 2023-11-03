USE museum_database;

-- Queries

-- 1)   Show all tables and explain how they are related to one another (keys, triggers, etc.)
SELECT  TABLE_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
FROM    INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE   REFERENCED_TABLE_SCHEMA = 'museum_database';

select  trigger_schema, trigger_name, EVENT_OBJECT_TABLE
from    information_schema.triggers
WHERE   trigger_schema = 'museum_database';

-- Art object a primary table where it contains information for primary keys for other tables and includes static values for each artwork, 
-- the artist talbe has a primary value that is connected to the art object table which gives information on the artist. THe exhibitions 
-- table is another primary table and displays information on an area where certain art pieces are contained the art objects and exibition 
-- tables are linked together with the displayed in table which takes the two key values of the art objects and exhibitions tables and 
-- connects them

-- 2)   A basic retrieval query

SELECT * 
FROM BORROWED;

-- 3)   A retrieval query with ordered results

SELECT  Name, Date_born, COO
FROM    ARTIST
ORDER BY Date_born ASC;

-- 4)   A nested retrieval query

SELECT  Title, Year, Artist
FROM    ART_OBJECT
WHERE   Id_no in    (
                    SELECT  ID_no 
                    FROM    DISPLAYED_IN
                    WHERE   Name = 'The Tudors: Art and Majesty in Renaissance England' 
                    );

-- 5)   A retrieval query using joined tables

SELECT AB.Id_no, Title, Year, Epoch, Artist, Date_acquired, Cost, Status
FROM ART_OBJECT AS AB
CROSS JOIN PERMANENT_C AS PC
WHERE AB.Id_no = PC.Id_no;

-- 6)   An update operation with any necessary triggers

UPDATE DISPLAYED_IN
SET Name = 'The Tudors: Art and Majesty in Renaissance England'
WHERE Name = 'Exhibition 1';

SELECT * 
FROM DISPLAYED_IN;

DROP TRIGGER IF EXISTS museum_database.update_trigger;

delimiter $$
CREATE TRIGGER update_trigger
BEFORE UPDATE ON PERMANENT_C
FOR EACH ROW 
BEGIN
    IF NEW.Cost < 0 THEN
        SET NEW.Cost = 0;
    END IF;
END$$
delimiter ;

UPDATE PERMANENT_C
SET Cost = -25000
WHERE Id_no = 003;

SELECT * 
FROM PERMANENT_C;

-- 7)   A deletion operation with any necessary triggers

DELETE FROM EXHIBITIONS
WHERE Name = 'Exhibition 1';

Select *
FROM EXHIBITIONS;

DROP TRIGGER IF EXISTS museum_database.delete_trigger;

delimiter $$
CREATE TRIGGER delete_trigger
BEFORE DELETE 
ON OTHER
FOR EACH ROW 
BEGIN
     SIGNAL SQLSTATE '45000'
     SET MESSAGE_TEXT = 'Invalid Deletion';
END$$
delimiter ;

DELETE FROM OTHER WHERE Id_no = 999;

SELECT *
FROM OTHER;

