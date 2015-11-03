drop schema if exists aurora;
create schema aurora collate utf8_general_ci;
use aurora;
create table if not exists users (geo varchar(100), chat_id int, geo_id int, kp_level int);
