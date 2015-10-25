drop schema if exists aurora;
create schema aurora;
use aurora;
create table if not exists users (geo varchar(100), chat_id int, geo_id int);