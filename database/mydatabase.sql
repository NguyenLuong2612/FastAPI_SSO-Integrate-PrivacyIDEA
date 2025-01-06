create database mydb;
use mydb;

create table account (
	id INT auto_increment,
    username  varchar(100) not null unique,
    password varchar(100) not null,
    create_at datetime,
    primary key(id)
);

create table person (
	personid int not null,
    full_name nvarchar(100),
    email nvarchar(100),
    constraint FK_PersonAccount foreign key (personid)
    references account(id)
);

