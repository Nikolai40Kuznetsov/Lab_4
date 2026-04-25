import pymssql
import credits as cr

conn = pymssql.connect(cr.server, cr.user, cr.password, cr.db)
cursor = conn.cursor()

cursor.execute ("""
USE ShopBd

CREATE TABLE GOODS(
	id INT IDENTITY(1, 1) PRIMARY KEY,
	[name] TEXT,
	[weight] FLOAT,
	terminate_date DATE
	)

CREATE TABLE GOODS_LIST(
	id INT IDENTITY(1, 1) PRIMARY KEY,
	goods INT,
	[status] TEXT,
	[count] INT,
	CONSTRAINT FK_1 FOREIGN KEY (goods) REFERENCES GOODS(id)
	)

CREATE TABLE LIST(
	id INT IDENTITY(1, 1) PRIMARY KEY,
	list INT
	CONSTRAINT FK_3 FOREIGN KEY (list) REFERENCES GOODS_LIST(id)
	)

CREATE TABLE STORAGE(
	id INT IDENTITY(1, 1) PRIMARY KEY,
	goods_list INT,
	available BIT
	CONSTRAINT FK_2 FOREIGN KEY (goods_list) REFERENCES LIST(id)
	)

CREATE TABLE LOGS(
	id INT IDENTITY(1, 1) PRIMARY KEY,
	[table] TEXT,
	op_type TEXT,
	date_time DATETIME
	)

GO
CREATE FUNCTION SELECT_GOODS_LIST()
RETURNS TABLE
AS
RETURN (SELECT GOODS_LIST.id, GOODS.[name], GOODS.[weight], 
		GOODS.terminate_date, GOODS_LIST.[count] FROM GOODS_LIST
		JOIN GOODS ON GOODS_LIST.goods = GOODS.id)
GO

GO
CREATE FUNCTION SELECT_STORAGE()
RETURNS TABLE
AS
RETURN (SELECT STORAGE.id, LIST.list, STORAGE.available FROM STORAGE
		JOIN LIST ON STORAGE.goods_list = LIST.id)
GO

GO
CREATE PROCEDURE INSERT_GOODS
@name TEXT,
@weight FLOAT,
@terminate_date DATE
AS
BEGIN
	INSERT INTO GOODS VALUES(@name, @weight, @terminate_date)
END
GO

CREATE TRIGGER ADD_TO_LIST
ON GOODS_LIST
FOR INSERT
AS
INSERT INTO LIST VALUES ((SELECT * FROM GOODS_LIST 
						  ORDER BY GOODS_LIST.id DESC))
"""
)


print(cursor.fetchall())
conn.commit()
conn.close()