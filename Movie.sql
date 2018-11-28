DROP TABLE IF EXISTS down;
DROP TABLE IF EXISTS movie;
DROP TABLE IF EXISTS category;

CREATE TABLE category (id int primary key auto_increment,
	title text);
    
CREATE TABLE movie (id int primary key auto_increment,
categorytitle text,
	title text,
    p text,
    details text,
    pubtime text,
	pic text,
	listpage text
);
    
CREATE TABLE down (id int primary key auto_increment,
	movietitle text,
	res text,
	detailpage text
);

select * from down order by id desc;
select * from movie order by id desc;
select * from category order by id desc;
