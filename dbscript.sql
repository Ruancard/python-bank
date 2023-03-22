create database banco;

\c banco;

create table accounts(
	doc varchar(11) not null,
	name varchar(200) not null,
	acc varchar(12) Primary key,
	office varchar(6) not null,
	credit integer,
	balance integer,
	password varchar(6) not null);

create table transaction(
	id serial Primary key,
	output varchar(15),
	input varchar(15),
	date TIMESTAMPTZ not null,
	valuation integer not null);

\dt;